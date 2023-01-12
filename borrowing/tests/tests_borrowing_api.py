import datetime
from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from borrowing.models import Borrowing
from book.tests.test_book_api import sample_book
from borrowing.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer
)

BORROWING_URL = reverse("borrowing:borrowing-list")


def sample_borrowing(**kwargs):
    defaults = {
        "expected_return_date": date.today(),
        "book_id": 1,
    }
    defaults.update(**kwargs)
    return Borrowing.objects.create(**defaults)


def detail_url(borrowing_id):
    return reverse("borrowing:borrowing-detail", args=[borrowing_id])


class UnauthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()  # No authentication

    def test_auth_required(self):
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_borrowing_unauthorized(self):
        sample_book()
        borrowing = {
            "expected_return_date": date.today(),
            "book_id": 1,
            "user_id": self.client
        }
        res = self.client.post(BORROWING_URL, borrowing)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()  # No authentication
        self.user_1 = get_user_model().objects.create_user(
            "test-user-1@user.com",
            "user12345",
        )
        self.client.force_authenticate(self.user_1)  # Create user_1 and loging

        self.user_2 = get_user_model().objects.create_user(
            "test-user-2@user.com",
            "user12345",
        )  # Create user_2

        self.admin = get_user_model().objects.create_user(
            "admin@admin.com",
            "admin12345",
            is_staff=True
        )  # Create admin-user

    def test_list_book_admin_all_list_user_only_your_own(self):
        sample_borrowing(user_id=self.user_1.id)  # create borrowing from user_1
        res_user_1 = self.client.get(BORROWING_URL)  # response for user_1

        self.client.force_authenticate(self.admin)  # login admin

        sample_borrowing(
            user_id=self.admin.id,
            expected_return_date=date.today() + datetime.timedelta(days=1),
            book_id=2
        )  # create borrowing from admin
        res_admin = self.client.get(BORROWING_URL)  # response for admin

        self.client.force_authenticate(self.user_1)  # login user_1

        self.assertNotEqual(res_user_1.data["results"], res_admin.data["results"])

    def test_filter_borrowing_by_user_id_and_is_active(self):
        borrowing_1 = sample_borrowing(user_id=self.user_1.id)
        borrowing_2 = sample_borrowing(
            user_id=self.user_2.id,
            actual_return_date=date.today(),
        )
        self.client.force_authenticate(self.admin)
        res = self.client.get(BORROWING_URL)

        res_with_filter = self.client.get(BORROWING_URL, {
            "user_id": f"{borrowing_2.user_id}",
            "is_active": f"{borrowing_2.is_active}",
        })  # Pass the search parameters

        serializer1 = BorrowingListSerializer(borrowing_1)
        serializer2 = BorrowingListSerializer(borrowing_2)

        self.assertIn(serializer1.data, res.data["results"])
        self.assertIn(serializer2.data, res_with_filter.data["results"])
        self.assertNotIn(serializer1.data, res_with_filter.data["results"])

    def test_retrieve_borrowing_detail(self):
        borrowing = sample_borrowing(user_id=self.user_1.id)

        url = detail_url(borrowing.id)
        res = self.client.get(url)

        serializer = BorrowingDetailSerializer(borrowing)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_borrowing(self):
        sample_book()

        borrowing = {
            "expected_return_date": date.today(),
            "book_id": 1,
            "user_id": self.user_1.id
        }

        res = self.client.post(BORROWING_URL, borrowing)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_delete_borrowing_forbidden_auth_user(self):
        sample_book()
        borrowing = sample_borrowing(user_id=self.user_1.id)

        url = detail_url(borrowing.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

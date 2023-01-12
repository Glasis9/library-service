from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from book.models import Book
from book.serializers import BookListSerializer

BOOK_URL = reverse("book:book-list")


def sample_book(**kwargs):
    defaults = {
        "title": "Test Book 248",
        "author": "Oleg",
        "cover": "Soft",
        "inventory": 2,
        "daily_fee": 10.01,
    }
    defaults.update(**kwargs)
    return Book.objects.create(**defaults)


def detail_url(book_id):
    return reverse("book:book-detail", args=[book_id])


class UnauthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_book_unauthorized(self):
        book = sample_book()
        url = detail_url(book.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_unauthorized(self):
        book = {
            "title": "Test Book 248",
            "author": "Oleg",
            "cover": "Soft",
            "inventory": 2,
            "daily_fee": 10.01,
        }

        res = self.client.post(BOOK_URL, book)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@user.com",
            "user12345",
        )
        self.client.force_authenticate(self.user)

    def test_delete_book_forbidden_auth_user(self):
        book = sample_book()
        url = detail_url(book.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_book(self):
        sample_book()

        res = self.client.get(BOOK_URL)

        books = Book.objects.all()
        serializer = BookListSerializer(books, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_filter_books_by_author_title_cover(self):
        book1 = sample_book()
        book2 = sample_book(
            author="Best Author",
            title="Metro 2033",
            cover="Soft"
        )
        res_1 = self.client.get(BOOK_URL)

        res_2 = self.client.get(BOOK_URL, {
            "author": f"{book2.author}",
            "title": f"{book2.title}",
            "cover": f"{book2.cover}"
        })  # Pass the search parameters

        serializer1 = BookListSerializer(book1)
        serializer2 = BookListSerializer(book2)

        self.assertIn(serializer1.data, res_1.data["results"])
        self.assertIn(serializer2.data, res_2.data["results"])
        self.assertNotIn(serializer1.data, res_2.data["results"])

    def test_retrieve_book_detail(self):
        book = sample_book()

        url = detail_url(book.id)
        res = self.client.get(url)

        serializer = BookListSerializer(book)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_book_forbidden(self):
        book = {
            "title": "Test Book 248",
            "author": "Oleg",
            "cover": "Soft",
            "inventory": 2,
            "daily_fee": 10.01,
        }

        res = self.client.post(BOOK_URL, book)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com",
            "admin12345",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_book(self):
        params = {
            "title": "Test Book 248",
            "author": "Oleg",
            "cover": "Soft",
            "inventory": 2,
            "daily_fee": Decimal(10),
        }

        res = self.client.post(BOOK_URL, params)
        book = Book.objects.get(id=res.data["id"])
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key in params:
            self.assertEqual(params[key], getattr(book, key))

    def test_delete_book_admin(self):
        book = sample_book()
        url = detail_url(book.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

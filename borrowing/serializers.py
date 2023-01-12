from datetime import date

from django.core.exceptions import ValidationError
from rest_framework import serializers

from book.models import Book
from borrowing.models import Borrowing

from library_service.notification import notification


class BorrowingSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(BorrowingSerializer, self).validate(attrs)
        queryset = Book.objects.get(id=attrs["book_id"])
        queryset.inventory -= 1
        if queryset.inventory >= 0:
            queryset.save()
            message = f"New borrowing:\n" \
                      f"Borrow date: {date.today()}\n" \
                      f"Expected return date: " \
                      f"{attrs['expected_return_date']}\n" \
                      f"Book id: {attrs['book_id']}, " \
                      f"title: {queryset.title}\n" \
                      f"User id: {self.context['request'].user.id}, " \
                      f"email: {self.context['request'].user}"
            notification(message)
            return data
        else:
            raise ValidationError("Book not available")

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id",
        )
        read_only_fields = ("id", "actual_return_date", "user_id")


class BorrowingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id",
            "is_active",
        )
        read_only_fields = (
            "id",
            "actual_return_date",
        )


class BorrowingDetailSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(BorrowingDetailSerializer, self).validate(attrs)
        if attrs["actual_return_date"] is not None:
            book_id = self.instance.book_id
            queryset = Book.objects.get(id=book_id)
            queryset.inventory += 1
            queryset.save()
            message = f"Borrowing complete: id: {self.instance.pk}\n" \
                      f"Borrow date: " \
                      f"{self.instance.borrow_date}\n" \
                      f"Expected return date: " \
                      f"{self.initial_data['expected_return_date']}\n" \
                      f"Actual return date: " \
                      f"{self.initial_data['actual_return_date']}\n" \
                      f"Book id: {book_id}, " \
                      f"title: {queryset.title}\n" \
                      f"User id: {self.context['request'].user.id}, " \
                      f"email: {self.context['request'].user}"
            notification(message)
            return data

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id",
            "is_active",
        )
        read_only_fields = ("id", "book_id", "user_id")

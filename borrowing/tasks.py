from datetime import date

from celery import shared_task
from django.db.models import Q

from borrowing.models import Borrowing
from book.models import Book
from user.models import User

from library_service.notification import notification


@shared_task()
def overdue_borrowings():
    queryset = Borrowing.objects.all().filter(
        Q(expected_return_date__lt=date.today()) & Q(actual_return_date=None)
    )
    if queryset.exists():
        for borrowing in queryset:
            book = Book.objects.get(id=borrowing.book_id)
            user = User.objects.get(id=borrowing.user_id)
            message = f"Overdue borrowing:\n" \
                      f"id: {borrowing.id}\n" \
                      f"Borrow date: {borrowing.borrow_date}\n" \
                      f"Expected return date: " \
                      f"{borrowing.expected_return_date}\n" \
                      f"Book id: {borrowing.book_id}, " \
                      f"Title: {book.title}\n" \
                      f"User id: {borrowing.user_id}, " \
                      f"email: {user.email}"
            notification(message)
    else:
        notification(message="No borrowings overdue today!")

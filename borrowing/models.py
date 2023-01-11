from django.db import models


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True)
    book_id = models.IntegerField()
    user_id = models.IntegerField()

    @property
    def is_active(self):
        return self.actual_return_date is None

    def __str__(self):
        return (
            f"Borrowing id: {self.id}, "
            f"Take: User_id: {self.user_id}, "
            f"Book: book_id: {self.book_id}. "
            f"Borrow date: {self.borrow_date}, "
            f"Expected return date: {self.expected_return_date}, "
            f"Actual return date: {self.actual_return_date}"
        )

    # @staticmethod
    # def complete_borrowing(pk: int):
    #     queryset = Borrowing.objects.get(id=pk)

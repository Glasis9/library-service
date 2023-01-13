from django.core.validators import MinValueValidator
from django.db import models


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "Hard"
        SOFT = "Soft"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=5, choices=CoverChoices.choices)
    inventory = models.IntegerField(validators=[MinValueValidator(1)])
    daily_fee = models.DecimalField(decimal_places=2, max_digits=6)

    def __str__(self) -> str:
        return (
            f"{self.title} (author: {self.author}), "
            f"cover: {self.cover}, "
            f"daily fee: {self.daily_fee_in_usd()}, "
            f"inventory: {self.inventory} "
        )

    def daily_fee_in_usd(self):
        return f"{self.daily_fee}$"

    class Meta:
        ordering = ["id"]

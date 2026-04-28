from django.db import models


class Movement(models.Model):
    class MovementType(models.TextChoices):
        CREDIT = "credit", "Credit"
        DEBIT = "debit", "Debit"

    description = models.CharField(max_length=255)
    movement_type = models.CharField(max_length=6, choices=MovementType.choices)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self) -> str:
        return str(self.description)

from django.db import models
from django.contrib.postgres.fields import IntegerRangeField
from django.contrib.postgres.validators import (
    RangeMaxValueValidator,
    RangeMinValueValidator
)

class StatusPercent(models.Model):
    SP_CHOICE ={
        "pending": "Pending",
        "reading": "Reading",
        "done": "Done"
    }
    percentage_read_range = IntegerRangeField(
        null=True,
        blank=True,
        validators = [RangeMinValueValidator(0), RangeMaxValueValidator(101)]
    )
    read_status = models.CharField(max_length=10, choices=SP_CHOICE, default='pending')

    class Meta:
        verbose_name_plural = 'Status Percentages'
        constraints = [
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_read_status_check',
                check=models.Q(read_status__in=['pending', 'reading', 'done'])
            )
        ]

    def __str__(self) -> str:
        # But when dealing with model's method, migration is not needed.
        return f'{self.percentage_read_range}({self.read_status})'
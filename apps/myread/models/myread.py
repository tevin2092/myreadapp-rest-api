from django.db import models

# Create your models here.

class MyRead(models.Model):
    book_isbn = models.ForeignKey('book.Book', on_delete=models.CASCADE)
    reader_username = models.ForeignKey('reader.Reader', on_delete=models.CASCADE)
    percentage_read  = models.PositiveSmallIntegerField(null=True, blank=True)
    start_read_date = models.DateField(null=True, blank=True)
    end_read_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('book_isbn', 'reader_username', 'start_read_date')
        constraints = [
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_per_read_check',
                check=models.Q(
                    percentage_read__gte=0,
                    percentage_read__lte=100
                    )
            ),
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_end_read_start_read_date_check',
                check=models.Q(end_read_date__gt=models.F('start_read_date'))
            ),
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_per_read_start_read_date_check',
                check=(
                    models.Q(
                        percentage_read__exact=0,
                        start_read_date__isnull=True
                    )
                    | models.Q(
                        percentage_read__gt=0,
                        start_read_date__isnull=False
                    )
                )
            ),
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_per_read_end_read_date_check',
                check=(
                    models.Q(
                        percentage_read__exact=100,
                        end_read_date__isnull=False
                    )
                    | models.Q(
                        percentage_read__lt=100,
                        end_read_date__isnull=True
                    )
                )
            ),

        ]

    def __str__(self) -> str:
        return f'{self.reader_username}({self.book_isbn})'
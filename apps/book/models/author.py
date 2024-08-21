from django.db import models

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'








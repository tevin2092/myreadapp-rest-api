from django.db import models 

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str: # pylint: disable=E0307
        return self.name
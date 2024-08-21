from datetime import timedelta
from django.db import models
# Create your models here.

class NIC(models.Model):
    nic_number = models.CharField(max_length=10, primary_key=True)
    delivery_date = models.DateField()
    # auto-calculated field from other fields
    # expiration_date = models.DateField()
    
    expiration_date = models.GeneratedField(
        expression = models.F('delivery_date') + timedelta(days=1827),
        output_field = models.DateField(),
        db_persist = True
    )

    def __str__(self) -> str:
        return f'{self.nic_number}(del: {self.delivery_date}, exp: {self.expiration_date})'
    
    class Meta:
        db_table_comment = 'National Identity Card'
        verbose_name_plural = 'NIC'
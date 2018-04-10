from django.db import models

# Create your models here.
class PaymentExtraItems(models.Model):
    name = models.CharField("Item Name", max_length=100)
    
    def __str__(self):
        return self.name
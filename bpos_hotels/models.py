from django.db import models

# Create your models here
HOTEL_TYPE_CHOICES = (
            ("standard", "Standard"),
            ("upgrade", "Upgrade"),
            ("luxury", "Luxury")
        )

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    town = models.ForeignKey(
        'bpos_towns.Town',
        on_delete=models.PROTECT, null=True)
    type = models.CharField(max_length=100, choices=HOTEL_TYPE_CHOICES)
    
    def __str__(self):
        return self.name + "(" + str(self.town) +")"
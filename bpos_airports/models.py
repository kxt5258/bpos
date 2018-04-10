from django.db import models
from django.core.validators import MinLengthValidator


# Create your models here.
class Airport(models.Model):
    name = models.CharField(max_length=200)
    shortkey = models.CharField(max_length=3, validators=[MinLengthValidator(3)])

    def __str__(self):
        return self.name + " (" + self.shortkey + " )"

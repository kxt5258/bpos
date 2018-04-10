from django.db import models
from django_countries.fields import CountryField


# Create your models here.
class Agent(models.Model):
    name = models.CharField(max_length=100)
    country = CountryField(blank_label='(Select Country)')

    def __str__(self):
        return self.name

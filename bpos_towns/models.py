from django.db import models

# Create your models here.
class Town(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name
from django.db import models

# Create your models here.
class Guide(models.Model):
    TREKKING_CHOICES = (
            ("1", "No Trekking License"),
            ("2", "No Trekking License, but does Trek"),
            ("3", "Trekking License")
        )
    
    LANGUAGUES_CHOICES = (
            ("french", "French"),
            ("chinese", "Chinese"),
            ("japanese", "Japanese"),
            ("german", "German"),
            ("spanish", "Spanish"),
            ("italian", "Italian"),
            ("russian", "Russian"),
            ("others", "Others")
        )
    
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    trekking_status = models.CharField("Trekking Status", max_length=100, choices=TREKKING_CHOICES, default='1')
    other_languages = models.CharField("Other Languages Speaking", max_length=100, choices=LANGUAGUES_CHOICES, blank=True)
    other_language = models.CharField("Other Language", max_length=100, blank=True)
    
    def __str__(self):
        return self.name + " (" + self.phone + ")"
    
    
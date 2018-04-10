from django.contrib import admin

# Register your models here.
from .models import Airport

class AirportAdmin(admin.ModelAdmin):
    list_display = ('name', 'shortkey')

admin.site.register(Airport, AirportAdmin)
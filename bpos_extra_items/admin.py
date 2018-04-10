from django.contrib import admin

# Register your models here.
from .models import ExtraItems

class ExtraItemsAdmin(admin.ModelAdmin):
    list_display = ('name')

admin.site.register(ExtraItems)
from django.contrib import admin

# Register your models here.
from .models import PaymentExtraItems

class PaymentExtraItemsAdmin(admin.ModelAdmin):
    list_display = ('name')

admin.site.register(PaymentExtraItems)
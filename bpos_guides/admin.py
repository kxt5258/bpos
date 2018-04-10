from django.contrib import admin

from .models import Guide

class GuideAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'trekking_status', 'other_languages', 'other_language')

admin.site.register(Guide, GuideAdmin)
from django.contrib import admin
from suit.admin import SortableModelAdmin
from .models import Town


class TownAdmin(SortableModelAdmin):
    sortable = 'order'
    list_display = ('name', 'order')
    
admin.site.register(Town, TownAdmin)
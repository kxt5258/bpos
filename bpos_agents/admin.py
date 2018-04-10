from django.contrib import admin

from .models import Agent

class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')

admin.site.register(Agent)
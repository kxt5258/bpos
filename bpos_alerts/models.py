from django.db import models
from bpos_status_report.models import Client
from django.contrib.auth.models import User


class Alert(models.Model):
    client = models.ForeignKey(Client, related_name="alerts")
    doctype = models.TextField(max_length=100, null=False, blank=False)
    changed_by = models.ForeignKey(User, related_name="alerts")
    changed_at = models.DateTimeField(null=False, blank=False)
    desc = models.TextField(max_length=200, null=True, blank=True)

    # Flight
    ttl = models.DateField(null=True, blank=True)

    # Hotel
    hotel_name = models.TextField(null=True, blank=True)
    hotel_status = models.TextField(null=True, blank=True)

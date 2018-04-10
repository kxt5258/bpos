from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create your models here.
class Enquiry(models.Model):
    STATUS_CHOICES = (
        ('enquiry', "Enquiry"),
        ('confirmed', "Confirmed"),
        ('cancelled', "Cancelled")
    )

    ACTION_TAKEN = (
        ("iti_sent", "Itinerary Sent"),
        ("info_sent", "Information Sent"),
        ("dis_iti", "Discussing Itinerary"),
        ("post_pone_trip", "Decided To Postpone Trip"),
        ("other", "Other")
    )

    readonly_fields = ("created_on", "confirmed_on",)

    first_name = models.CharField("First Name", max_length=100, blank=True)
    last_name = models.CharField("Last Name", max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    source = models.CharField(max_length=100, blank=True)
    planned_trip = models.CharField("Planned Trip", max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enquiry')
    action_taken = models.CharField("Action Taken", max_length=100, choices=ACTION_TAKEN)
    other_action = models.CharField("Other Action Taken", max_length=100, blank=True)
    is_monitored = models.BooleanField("Is Monitored")
    created_on = models.DateField("Created On", blank=True, null=True)
    confirmed_on = models.DateField("Confirmed On", blank=True, null=True)
    full_name = models.CharField("Full Name", max_length=200, blank=True)
    contact = models.CharField(max_length=200, blank=True)
    client_id = models.PositiveSmallIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.created_on:
            self.created_on = timezone.now()
        if self.status == "confirmed" and not self.confirmed_on:
            self.confirmed_on = timezone.now()

        self.full_name = self.first_name + " " + self.last_name

        if self.email and self.phone:
            self.contact = self.email + "/" + self.phone
        elif self.email:
            self.contact = self.email
        else:
            self.contact = self.phone

        return super(Enquiry, self).save(*args, **kwargs)

    class Meta:
        ordering = ['created_on']

    def get_absolute_url(self):
        return reverse('enquiry-list')

    def __str__(self):
        return self.full_name

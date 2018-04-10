from django.db import models

from django.urls import reverse
from django.db.models.fields.related import ForeignKey

from bpos_agents.models import Agent
from bpos_enquiries.models import Enquiry

# Create your models here.
TITLE = (("mr", "Mr"), ("mrs", "Mrs"), ("ms", "Ms"), ("master", "Master"), ("miss", "Miss"))


class Client(models.Model):
    TYPE_CHOICES = (('fit', "FIT"), ('group', "Group"))
    TREK_CHOICES = (('bumdra', 'Bumdra'), ('dagala', 'Dagala'), ('other', 'Other'))
    LANGAUGE_CHOICES = (('french', "French"), ('chinese', 'Chinese'), ('japanese', 'Japanese'), ('other', 'Other'))
    OPTIONS_STATUS = (('0', ''), ('1', 'Passport On System'), ('2', 'Visa Applied For'), ('3', 'Visa Authorised'), ('4', 'Visa Sent To Client'))

    agent = models.ForeignKey(Agent, related_name="clients")
    type = models.CharField(max_length=50, blank=False, choices=TYPE_CHOICES, default='fit')
    group_name = models.CharField(max_length=100, blank=False)
    name = models.CharField(max_length=150, blank=False)
    pax = models.PositiveSmallIntegerField(default=1)
    arriving_date = models.DateField("Arriving On", null=False, blank=False)
    leaving_date = models.DateField("Leaving On", null=False, blank=False)
    entering_from = models.CharField("Entering From", max_length=100)
    leaving_to = models.CharField("Leaving To", max_length=100)
    trek = models.CharField(max_length=100, choices=TREK_CHOICES, blank=True)
    other_trek = models.CharField("Other Trek", max_length=300, blank=True)
    guide_notified = models.BooleanField("Guide Notified to Client?", blank=True, default=False)
    language_guide_needed = models.BooleanField("Language Guide Needed?", blank=True)
    language = models.CharField("Choose Language Needed", max_length=100, choices=LANGAUGE_CHOICES, blank=True)
    other_language = models.CharField("Other Language", max_length=100, blank=True)
    flight_status = models.CharField("Flight Status", max_length=100, blank=True)
    payment_status = models.CharField("Money Status", max_length=100, blank=True)
    hotel_status = models.CharField("Hotel Status", max_length=100, blank=True)
    visa_status = models.CharField("Visa Status", max_length=100, blank=True)
    guide = models.CharField("Guide", max_length=200, blank=True)
    is_archive = models.BooleanField(blank=True, default=0)
    status = models.CharField(max_length=2, blank=True, null=True, choices=OPTIONS_STATUS, default='0')
    enquiry = models.ForeignKey(Enquiry, related_name="clients", null=True, blank=True)

    def save(self, *args, **kwargs):
        self.name = str(self.agent) + " " + self.type + " - " + self.group_name
        if not self.flight_status:
            self.flight_status = "Not Yet Requested"

        if not self.hotel_status:
            self.hotel_status = "Not Yet Requested"

        return super(Client, self).save(*args, **kwargs)

    class Meta:
        ordering = ['arriving_date']

    def __str__(self):
        return "%s (id=%s)" % (self.name, self.id)

    def get_absolute_url(self):
        return reverse('client-detail', kwargs={'pk': self.id})


class Member(models.Model):
    client = ForeignKey(Client)
    full_name = models.CharField(max_length=200, null=False, blank=False)
    title = models.CharField(max_length=20, choices=TITLE)
    is_student = models.BooleanField("Is Student")

    def __str__(self):
        return "%s. %s (id: %s) " % (self.get_title_display(), self.full_name, self.id)


class Document(models.Model):
    DOC_TYPE_CHOICES = (('pass', "Passport"), ('v_info', "Visa Info"), ('stu', "Student ID"), ('visa', "Visa"))
    client = ForeignKey(Client)
    document_for = models.ForeignKey(Member)
    document_type = models.CharField("Document Type", max_length=30, choices=DOC_TYPE_CHOICES)
    comment = models.TextField(null=True, blank=True)
    visa_alert = models.BooleanField("Send Alert to Visas")
    ticket_alert = models.BooleanField("Send Alert to Ticketing")
    document = models.FileField(upload_to='documents/', blank=True)

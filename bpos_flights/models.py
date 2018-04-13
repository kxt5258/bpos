from django.db import models
from bpos_status_report.models import Client, Member
from bpos_airports.models import Airport
from bpos_status_report.models import TITLE
from bpos_alerts.models import Alert

from django_currentuser.middleware import get_current_authenticated_user

from django.utils import timezone

FARE_OPTIONS = (
    ("full", "Full Fare"),
    ("excursion", "Excursion Fare"),
    ("low", "Low Season Discount"),
    ("other", "Other")
)

FLIGHT_CLASS = (
    ("y", "Y CLass"),
    ("j", "J CLass"),
    ("s", "S CLass")
)

FLIGHT_STATUS = (
    ("0", "Not Yet Requested"),
    ("1", "Requested"),
    ("2", "Confirmed"),
    ("3", "Waitlisted"),
    ("4", "Tickets Issued"),
    ("5", "Tickets Sent")
)


# Create your models here.
class Flight(models.Model):
    client = models.ForeignKey(Client)
    passenger = models.ForeignKey(Member)
    title = models.CharField(max_length=10, choices=TITLE)
    full_name = models.CharField("Full Name", max_length=100, blank=False)
    dob = models.DateField("Date of Birth")
    is_student = models.BooleanField("Is Student?")
    fare = models.CharField(max_length=100, choices=FARE_OPTIONS, blank=False, default="full")
    other_fare = models.CharField("Other Fare", max_length=100, blank=True)
    from_place = models.ForeignKey(Airport, related_name="flight_from_place")
    to_place = models.ForeignKey(Airport, related_name="flight_to_place")
    date = models.DateField("Flight Date")
    flight_no = models.CharField("Specific Flight Number", max_length=20, blank=True)
    flight_class = models.CharField("Class", max_length=20, choices=FLIGHT_CLASS)
    status = models.CharField(max_length=100, choices=FLIGHT_STATUS, default="0")
    ttl = models.DateField("TTL", max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.full_name)

    def __init__(self, *args, **kwargs):
        super(Flight, self).__init__(*args, **kwargs)
        self._ori_ttl = self.ttl
        self._ori_status = self.status

    def save(self, *args, **kwargs):
        desc = ""
        update = 0

        if not self._ori_ttl and self.ttl:
            desc = "TTL Added"
            update = 1
        elif self._ori_ttl and self._ori_ttl != self.ttl:
            desc = "TTL Changed"
            update = 1
        else:
            pass

        if self._ori_status and self._ori_status != self.status and self.status not in (0, 4, 5):
            desc = "Flight " + str(FLIGHT_STATUS[int(self.status)][1]) + " for " + str(self.date)
            update = 1
        elif self._ori_status and self._ori_status != self.status and self.status in (4, 5):
            desc = str(FLIGHT_STATUS[int(self.status)][1]) + " for " + str(self.date)
            update = 1
        else:
            pass

        if update:
            alert_data = {
                "client": self.client,
                "doctype": "Flight",
                "changed_by": get_current_authenticated_user(),
                "changed_at": timezone.now(),
                "desc": desc,
                "ttl": self.ttl
            }
            Alert(**alert_data).save()

        super(Flight, self).save(*args, **kwargs)


class FlightGroup(models.Model):
    client = models.ForeignKey(Client)
    pax = models.IntegerField()
    comments = models.TextField(null=True, blank=True)

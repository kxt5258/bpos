from django.db import models
from bpos_status_report.models import Client
from bpos_towns.models import Town
from bpos_hotels.models import Hotel, HOTEL_TYPE_CHOICES

FOOD_OPTIONS = (('1', 'Bed and Breakfast'), ('2', 'Bed, Breakfast and Dinner'), ('3', 'Full Board'))
ROOM_TYPE = (('single', 'Single'), ('double', 'Double'), ('twin', 'Twin'))
ROOM_CAT = (
    ('1', 'Superior'),
    ('2', 'Deluxe'),
    ('3', 'Luxury'),
    ('4', 'Junior Suite'),
    ('5', 'Suite'),
    ('6', 'One Bed Villa'),
    ('7', 'Two Bed Villa'),
    ('8', 'Other')
)
ROOM_STATUS = (('1', 'Not Yet Requested'), ('2', 'Requested'), ('3', 'Waiting'), ('4', 'Confirmed'))


# Create your models here.
class HotelReservation(models.Model):
    client = models.ForeignKey(Client)
    town = models.ForeignKey(Town)
    arriving_on = models.CharField("Arriving On", max_length=20)
    leaving_on = models.CharField("Leaving On", max_length=20)
    hotel_type = models.CharField(max_length=100, choices=HOTEL_TYPE_CHOICES)
    hotel_name = models.ForeignKey(Hotel)
    food_option = models.CharField(max_length=100, choices=FOOD_OPTIONS, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    is_backup = models.BooleanField("Is Backup")

    def __str__(self):
        return str(self.hotel_name)


class Room(models.Model):
    hotel = models.ForeignKey(HotelReservation)
    date = models.DateField()
    room_type = models.CharField("Room Type", choices=ROOM_TYPE, max_length=10)
    room_category = models.CharField("Room Category", choices=ROOM_CAT, max_length=10)
    other_category = models.CharField("Other Room Category", max_length=100, blank=True, null=True)
    quantity = models.PositiveSmallIntegerField("Quantity")
    extra_bed = models.CharField("Extra Bed", max_length=100, null=True, blank=True)
    room_status = models.CharField("Room Status", choices=ROOM_STATUS, max_length=10)
    is_backup = models.BooleanField("Is backup")

    def __str__(self):
        return str(self.hotel) + "(" + str(self.date) + ")"

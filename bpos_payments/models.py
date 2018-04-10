from django.db import models
from bpos_status_report.models import Client
from bpos_extra_items.models import ExtraItems
from bpos_payment_out_items.models import PaymentExtraItems

PAYMENT_STATUS = (
    ('1', 'Pay Information Sent'),
    ('2', 'Invoice Sent'),
    ('3', 'Money Sent'),
    ('4', 'Money Received')
)
MONEY_OPTION = (
    ('1', 'Money To Refund'),
    ('2', 'Money To Collect')
)


# Create your models here.
class Payment(models.Model):
    client = models.ForeignKey(Client)
    '''Tour Price'''
    tour = models.FloatField("Tour", blank=True, default=0.00)
    flight = models.FloatField("Flight", blank=True, default=0.00)
    visa = models.FloatField("Visa fees", blank=True, default=0.00)
    bank = models.FloatField("Bank Charges", blank=True, default=0.00)
    flight_estimated = models.BooleanField("Is Flight Estimated")
    '''Payment'''
    deposit = models.CharField(max_length=2, blank=True, choices=PAYMENT_STATUS)
    balance = models.CharField(max_length=2, blank=True, choices=PAYMENT_STATUS)
    payment = models.CharField(max_length=2, blank=True, choices=PAYMENT_STATUS)
    la_date = models.CharField("Date of Last Action", max_length=100, blank=True)
    bank_form = models.FileField(upload_to='documents/', blank=True)
    amount_received = models.CharField("Amount Received and Rate", max_length=200, blank=True)
    '''Money pay and Collect'''
    money_owed = models.CharField("Money Owed", max_length=2, choices=MONEY_OPTION, blank=True)
    amount = models.FloatField(blank=True, null=True, default=0.00)
    paid = models.BooleanField("Money Paid to Client")
    collected = models.BooleanField("Money Collected from Client")
    '''Cancellation'''
    group_cancelled = models.BooleanField("Group Cancelled")
    member_cancelled = models.BooleanField("Group Member Cancelled")
    refund = models.FloatField("Amount Refunded", blank=True, null=True, default=0.00)

    def __str__(self):
        return "Payment for " + str(self.client)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('payment-detail', args=[str(self.id)])


class PayExtraItem(models.Model):
    client = models.ForeignKey(Client, null=True)
    item = models.ForeignKey(ExtraItems)
    amount = models.FloatField()

    def __str__(self):
        return str(self.item) + "(" + str(self.amount) + ")"


class PayPaymentOut(models.Model):
    client = models.ForeignKey(Client, null=True)
    item = models.ForeignKey(PaymentExtraItems)
    amount = models.FloatField()
    paid = models.BooleanField(blank=True)

    def __str__(self):
        return str(self.item) + "(" + str(self.amount) + ")"

from django.db import models

from bpos_status_report.models import Client
from bpos_guides.models import Guide

OPTIONS = (
    ("0", "All Guides"),
    ("3", "Has Trekking Licence "),
    ("2", "No Trekking Licence, but does Trek ")
)


class GroupGuide(models.Model):
    guide_filter = models.CharField(max_length=50, blank=False, choices=OPTIONS, default="0")
    client = models.ForeignKey(Client)
    guide = models.ForeignKey(Guide, null=True, blank=True)
    available = models.BooleanField("Available?")
    confirmed = models.BooleanField("Confirmed?")
    language = models.CharField("Language", max_length=200, blank=True, null=True)
    trek = models.CharField("Trek", max_length=200, blank=True, null=True)

    class Meta:
        permissions = (
            ('change_groupguide_confirmed', 'Change Confirmed of Guide'),
        )

    def save(self, *args, **kwargs):
        if self.confirmed:
            client = Client.objects.get(pk=self.client.id)
            if client.guide:
                match = False
                for a in client.guide.split(","):
                    print(a)
                    if a == self.guide.__str__():
                        match = True
                        break
                if not match:
                    client.guide = (client.guide + " , " + self.guide.__str__())
            else:
                client.guide = self.guide.__str__()
            client.save()

        return super(GroupGuide, self).save(*args, **kwargs)

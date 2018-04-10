from django.core.management.base import BaseCommand
from bpos_status_report.models import Client
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Archives the Client after the leaving date"

    def handle(self, *args, **options):
        clients = Client.objects.filter(is_archive=0).order_by("id")
        for client in clients:
            date = client.arriving_date + timedelta(days=14)
            if date < datetime.now().date():
                obj = Client.objects.get(pk=client.pk)
                obj.is_archive = 1
                obj.save()
                print("Arhiving " + str(client.pk))

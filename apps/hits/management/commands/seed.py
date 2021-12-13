import os, csv, re

# Django
from django.core.management.base import BaseCommand
from django.core.management import call_command

# Models
from apps.authentication.models import User


class Command(BaseCommand):
    help = "Seed application"

    def handle(self, *args, **options):
        path = os.path.dirname(__file__) + "/../data/data-hitmen.csv"
        if not User.objects.all():
            with open(path) as read_file:
                csv_reader = csv.reader(read_file, delimiter=",")
                for row in csv_reader:
                    pk = int(row[0])
                    username = row[1]
                    first_name = row[2]
                    last_name = row[3]
                    email = row[4]
                    password = row[5]
                    boss = int(row[6])
                    data = {
                        "username": username,
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "is_active": True,
                        "password": password,
                    }
                    if pk == 1:
                        data.update({"is_superuser": True})
                    if pk in (2, 3, 4):
                        data.update({"is_staff": True})
                    if boss > 0:
                        data.update({"boss_id": boss})
                    user = User.objects.create_user(**data)
            read_file.close()
        self.stdout.write(self.style.SUCCESS("Successfully init data"))

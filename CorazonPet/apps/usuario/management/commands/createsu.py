from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username="Corazonpetadmin2").exists():
            User.objects.create_superuser("Corazonpetadmin2", "corazonpet@gmail.com", "Corazonpet2017")

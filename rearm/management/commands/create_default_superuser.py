from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Create default superuser if none exists'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'SuperAdminRearm')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'reaarm22@gmail.com')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'SuperAdminRearm2025@')

        if not username or not email or not password:
            self.stdout.write(self.style.ERROR('Superuser environment variables not set.'))
            return

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created.'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists.'))

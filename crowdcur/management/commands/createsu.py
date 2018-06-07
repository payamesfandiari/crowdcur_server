from django.core.management.base import BaseCommand, CommandError
from accounts.models import User


class Command(BaseCommand):
    help = 'Creates a Super User if does not exist.'

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin2").exists():
            User.objects.create_superuser(username="admin2",
                                          email="me76@njit.edu",
                                          password="payam123",
                                          )
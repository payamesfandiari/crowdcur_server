from django.core.management.base import BaseCommand, CommandError
from accounts.models import User


class Command(BaseCommand):
    help = 'Creates a Super User if does not exist.'

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(username="admin",
                                          email="me76@njit.edu",
                                          password="lk`hlisjl123",
                                          )
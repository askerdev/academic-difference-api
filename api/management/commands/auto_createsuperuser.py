"""
This command will create a new superuser with the given email and password.
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    """Command to create a new superuser with the given email and password."""

    help = "Create a superuser with predefined credentials"

    def add_arguments(self, parser):
        """Argument parser."""
        parser.add_argument(
            "--username", type=str, help="Username for the superuser"
        )
        parser.add_argument("--email", type=str, help="Email for the superuser")
        parser.add_argument(
            "--password", type=str, help="Password for the superuser"
        )

    def handle(self, *args, **options):
        """Command line handler."""

        username = options["username"]
        email = options["email"]
        password = options["password"]

        if not all([username, email, password]):
            self.stdout.write(
                self.style.ERROR(
                    "Username, email, and password must be provided."
                )
            )
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Superuser "{username}" already exists.')
            )
        else:
            User.objects.create_superuser(
                username=username, email=email, password=password
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Superuser "{username}" created successfully.'
                )
            )

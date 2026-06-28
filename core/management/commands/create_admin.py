from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
import getpass


User = get_user_model()


class Command(BaseCommand):
    help = "Create an admin user for the SIO RT Nagar API"

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            type=str,
            help="Email address for the admin user",
        )
        parser.add_argument(
            "--username",
            type=str,
            help="Username for the admin user",
        )
        parser.add_argument(
            "--password",
            type=str,
            help="Password for the admin user (not recommended for production)",
        )
        parser.add_argument(
            "--noinput",
            action="store_true",
            help="Do not prompt for input (use with --email, --username, --password)",
        )

    def handle(self, *args, **options):
        email = options.get("email")
        username = options.get("username")
        password = options.get("password")
        noinput = options.get("noinput")

        if noinput:
            if not email or not username or not password:
                raise CommandError(
                    "When using --noinput, you must provide --email, --username, and --password"
                )
        else:
            # Interactive mode
            if not email:
                email = input("Email: ").strip()
            if not username:
                username = input("Username: ").strip()
            if not password:
                password = getpass.getpass("Password: ")
                password_confirm = getpass.getpass("Confirm Password: ")
                if password != password_confirm:
                    raise CommandError("Passwords do not match")

        # Validate inputs
        if not email:
            raise CommandError("Email is required")
        if not username:
            raise CommandError("Username is required")
        if not password:
            raise CommandError("Password is required")
        if len(password) < 8:
            raise CommandError("Password must be at least 8 characters long")

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            raise CommandError(f"User with email '{email}' already exists")
        if User.objects.filter(username=username).exists():
            raise CommandError(f"User with username '{username}' already exists")

        # Create the admin user
        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created admin user: {username} ({email})"
                )
            )
        except Exception as e:
            raise CommandError(f"Failed to create admin user: {str(e)}")

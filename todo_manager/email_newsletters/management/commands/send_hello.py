from django.core.mail import send_mail
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Send example hello email"

    def handle(self, *args, **options):
        self.stdout.write("Send email")

        send_mail(
            "Welcome Subject!",
            "This is message body! Glad to see you.",
            "admin@admin.com",
            ["recipient@example.com"],
            fail_silently=False,
        )

        self.stdout.write(self.style.SUCCESS("Email sent"))

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Send example hello email"

    def handle(self, *args, **options):
        self.stdout.write("Send complex email")

        name = "John Smith"
        subject = f"Welcome, {name}!"
        sender = "admin@admin.com"
        recipient = "john@example.com"

        context = {
            "name": name,
        }
        # First, render the plain text content.
        text_content = render_to_string(
            template_name="email_newsletters/welcome_message.txt",
            context=context,
        )

        # Secondly, render the HTML content.
        html_content = render_to_string(
            template_name="email_newsletters/welcome_message.html",
            context=context,
        )

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=sender,
            to=[recipient],
            headers={"List-Unsubscribe": "<mailto:unsub@example.com>"},
        )

        # Lastly, attach the HTML content to the email instance and send.
        msg.attach_alternative(html_content, "text/html")

        # Finally send email
        msg.send()

        self.stdout.write(self.style.SUCCESS("Complex email sent"))

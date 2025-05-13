# newsletters/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Newsletter, Attempt


@shared_task
def send_newsletter(newsletter_id):
    try:
        newsletter = Newsletter.objects.get(id=newsletter_id)
        for recipient in newsletter.recipients.all():
            try:
                send_mail(
                    newsletter.message.subject,
                    newsletter.message.body,
                    "rilz.snep@yandex.ru",
                    [recipient.email],
                    fail_silently=False,
                )
                Attempt.objects.create(
                    newsletter=newsletter,
                    status="successful",
                    server_response="Email sent successfully",
                )
            except Exception as e:
                Attempt.objects.create(
                    newsletter=newsletter, status="failed", server_response=str(e)
                )
    except Newsletter.DoesNotExist:
        pass


@shared_task
def update_newsletter_statuses():
    now = timezone.now()
    newsletters = Newsletter.objects.all()
    for newsletter in newsletters:
        if newsletter.end_time < now and newsletter.status != "completed":
            newsletter.status = "completed"
            newsletter.save()
        elif newsletter.start_time <= now and newsletter.status == "created":
            newsletter.status = "started"
            newsletter.save()

# newsletters/models.py
from django.conf import settings
from django.db import models


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="messages"
    )

    def __str__(self):
        return self.subject

    class Meta:
        permissions = [
            ("can_view_all_messages", "Can view all messages"),
        ]


class Recipient(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True, null=True)  # Добавляем null=True
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recipients"
    )

    def __str__(self):
        return self.email

    class Meta:
        permissions = [
            ("can_view_all_recipients", "Can view all recipients"),
        ]


class Newsletter(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    STATUS_CHOICES = [
        ("created", "Создана"),
        ("started", "Запущена"),
        ("completed", "Завершена"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="created")
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient, related_name="newsletters")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="newsletters"
    )

    def __str__(self):
        return f"Newsletter {self.id} - {self.status}"

    class Meta:
        permissions = [
            ("can_view_all_newsletters", "Can view all newsletters"),
            ("can_disable_newsletters", "Can disable newsletters"),
        ]


class Attempt(models.Model):
    attempt_time = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ("successful", "Успешно"),
        ("failed", "Не успешно"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    server_response = models.TextField(null=True, blank=True)
    newsletter = models.ForeignKey(
        Newsletter, on_delete=models.CASCADE, related_name="attempts"
    )

    def __str__(self):
        return f"Attempt for {self.newsletter} at {self.attempt_time}"

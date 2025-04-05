from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser


class Recipient(models.Model):
    full_name = models.CharField(max_length=255, verbose_name=_("Full Name"))
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    comment = models.TextField(blank=True, null=True, verbose_name=_("Comment"))
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="recipients",
        verbose_name=_("Owner"),
    )

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    class Meta:
        verbose_name = _("Recipient")
        verbose_name_plural = _("Recipients")


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name=_("Subject"))
    body = models.TextField(verbose_name=_("Body"))
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name=_("Owner"),
    )

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")


class Newsletter(models.Model):
    FREQUENCY_CHOICES = (
        ("daily", _("Daily")),
        ("weekly", _("Weekly")),
        ("monthly", _("Monthly")),
    )
    STATUS_CHOICES = (
        ("created", _("Created")),
        ("started", _("Started")),
        ("finished", _("Finished")),
    )

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="newsletters",
        verbose_name=_("Message"),
    )
    recipients = models.ManyToManyField(
        Recipient, related_name="newsletters", verbose_name=_("Recipients")
    )
    start_time = models.DateTimeField(verbose_name=_("Start Time"))
    end_time = models.DateTimeField(verbose_name=_("End Time"))
    frequency = models.CharField(
        max_length=10,
        choices=FREQUENCY_CHOICES,
        default="daily",
        verbose_name=_("Frequency"),
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="created",
        verbose_name=_("Status"),
    )
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="newsletters",
        verbose_name=_("Owner"),
    )

    def __str__(self):
        return f"Newsletter for {self.message.subject} ({self.start_time} - {self.end_time})"

    class Meta:
        verbose_name = _("Newsletter")
        verbose_name_plural = _("Newsletters")


class Attempt(models.Model):
    STATUS_CHOICES = (
        ("success", _("Success")),
        ("failed", _("Failed")),
    )

    newsletter = models.ForeignKey(
        Newsletter,
        on_delete=models.CASCADE,
        related_name="attempts",
        verbose_name=_("Newsletter"),
    )
    attempt_time = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Attempt Time")
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, verbose_name=_("Status")
    )
    server_response = models.TextField(
        blank=True, null=True, verbose_name=_("Server Response")
    )

    def __str__(self):
        return f"Attempt for {self.newsletter} at {self.attempt_time}"

    class Meta:
        verbose_name = _("Attempt")
        verbose_name_plural = _("Attempts")

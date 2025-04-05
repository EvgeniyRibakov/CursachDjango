from django.contrib import admin
from .models import Recipient, Message, Newsletter, Attempt


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "owner")
    list_filter = ("owner",)
    search_fields = ("full_name", "email")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "owner")
    list_filter = ("owner",)
    search_fields = ("subject",)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("message", "start_time", "end_time", "frequency", "status", "owner")
    list_filter = ("frequency", "status", "owner")
    search_fields = ("message__subject",)


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ("newsletter", "attempt_time", "status")
    list_filter = ("status",)
    search_fields = ("newsletter__message__subject",)

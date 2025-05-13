# newsletters/admin.py
from django.contrib import admin
from .models import Message, Recipient, Newsletter, Attempt


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["subject", "owner"]
    list_filter = ["owner"]
    search_fields = ["subject"]


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ["email", "full_name", "owner"]
    list_filter = ["owner"]
    search_fields = ["email", "full_name"]


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ["id", "start_time", "end_time", "status", "owner"]
    list_filter = ["status", "owner"]
    search_fields = ["message__subject"]


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ["attempt_time", "status", "newsletter"]
    list_filter = ["status"]
    search_fields = ["server_response"]

# newsletters/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.views.decorators.cache import cache_page
from django.db.models import Count
from .models import Message, Recipient, Newsletter, Attempt


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "newsletters/newsletters/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["total_newsletters"] = Newsletter.objects.filter(owner=user).count()
        context["active_newsletters"] = Newsletter.objects.filter(
            owner=user, status="started"
        ).count()
        context["unique_recipients"] = (
            Recipient.objects.filter(owner=user).distinct().count()
        )
        return context


class ReportView(LoginRequiredMixin, TemplateView):
    template_name = "newsletters/newsletters/report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        attempts = Attempt.objects.filter(newsletter__owner=user)
        context["total_attempts"] = attempts.count()
        context["successful_attempts"] = attempts.filter(status="successful").count()
        context["failed_attempts"] = attempts.filter(status="failed").count()
        context["newsletters"] = Newsletter.objects.filter(owner=user).annotate(
            attempt_count=Count("attempt")
        )
        return context


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "newsletters/newsletters/message_list.html"

    @cache_page(60 * 15)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "newsletters/newsletters/message_form.html"
    success_url = reverse_lazy("message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "newsletters/newsletters/message_form.html"
    success_url = reverse_lazy("message_list")

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "newsletters/newsletters/message_confirm_delete.html"
    success_url = reverse_lazy("message_list")

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = "newsletters/newsletters/recipient_list.html"

    @cache_page(60 * 15)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Recipient.objects.filter(owner=self.request.user)


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    fields = ["email", "full_name", "comment"]
    template_name = "newsletters/newsletters/recipient_form.html"
    success_url = reverse_lazy("recipient_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    fields = ["email", "full_name", "comment"]
    template_name = "newsletters/newsletters/recipient_form.html"
    success_url = reverse_lazy("recipient_list")

    def get_queryset(self):
        return Recipient.objects.filter(owner=self.request.user)


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = "newsletters/newsletters/recipient_confirm_delete.html"
    success_url = reverse_lazy("recipient_list")

    def get_queryset(self):
        return Recipient.objects.filter(owner=self.request.user)


class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter
    template_name = "newsletters/newsletters/newsletter_list.html"

    @cache_page(60 * 15)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Newsletter.objects.filter(owner=self.request.user)


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    fields = ["start_time", "end_time", "status", "message", "recipients"]
    template_name = "newsletters/newsletters/newsletter_form.html"
    success_url = reverse_lazy("newsletter_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    fields = ["start_time", "end_time", "status", "message", "recipients"]
    template_name = "newsletters/newsletters/newsletter_form.html"
    success_url = reverse_lazy("newsletter_list")

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    model = Newsletter
    template_name = "newsletters/newsletters/newsletter_confirm_delete.html"
    success_url = reverse_lazy("newsletter_list")

    def get_queryset(self):
        return Newsletter.objects.filter(owner=self.request.user)


class AttemptListView(LoginRequiredMixin, ListView):
    model = Attempt
    template_name = "newsletters/newsletters/attempt_list.html"

    @cache_page(60 * 15)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Attempt.objects.filter(newsletter__owner=self.request.user)


class ManagerNewsletterListView(PermissionRequiredMixin, ListView):
    model = Newsletter
    template_name = "newsletters/newsletters/manager_newsletter_list.html"
    permission_required = "newsletters.can_view_all_newsletters"

    def get_queryset(self):
        return Newsletter.objects.all()

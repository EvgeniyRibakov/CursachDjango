from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Recipient, Message, Newsletter, Attempt


class ManagerOrOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_manager() or obj.owner == self.request.user


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = "recipient_list.html"  # Обновлено

    def get_queryset(self):
        if self.request.user.is_manager():
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=self.request.user)


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    fields = ["full_name", "email", "comment"]
    template_name = "recipient_form.html"  # Обновлено
    success_url = reverse_lazy("recipient_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, ManagerOrOwnerMixin, UpdateView):
    model = Recipient
    fields = ["full_name", "email", "comment"]
    template_name = "recipient_form.html"  # Обновлено
    success_url = reverse_lazy("recipient_list")


class RecipientDeleteView(LoginRequiredMixin, ManagerOrOwnerMixin, DeleteView):
    model = Recipient
    template_name = "recipient_confirm_delete.html"  # Обновлено
    success_url = reverse_lazy("recipient_list")


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "message_list.html"  # Обновлено

    def get_queryset(self):
        if self.request.user.is_manager():
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "message_form.html"  # Обновлено
    success_url = reverse_lazy("message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, ManagerOrOwnerMixin, UpdateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "message_form.html"  # Обновлено
    success_url = reverse_lazy("message_list")


class MessageDeleteView(LoginRequiredMixin, ManagerOrOwnerMixin, DeleteView):
    model = Message
    template_name = "message_confirm_delete.html"  # Обновлено
    success_url = reverse_lazy("message_list")


class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter
    template_name = "newsletter_list.html"  # Обновлено

    def get_queryset(self):
        if self.request.user.is_manager():
            return Newsletter.objects.all()
        return Newsletter.objects.filter(owner=self.request.user)


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    fields = ["message", "recipients", "start_time", "end_time", "frequency", "status"]
    template_name = "newsletter_form.html"  # Обновлено
    success_url = reverse_lazy("newsletter_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_manager():
            form.fields["message"].queryset = Message.objects.filter(
                owner=self.request.user
            )
            form.fields["recipients"].queryset = Recipient.objects.filter(
                owner=self.request.user
            )
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, ManagerOrOwnerMixin, UpdateView):
    model = Newsletter
    fields = ["message", "recipients", "start_time", "end_time", "frequency", "status"]
    template_name = "newsletter_form.html"  # Обновлено
    success_url = reverse_lazy("newsletter_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_manager():
            form.fields["message"].queryset = Message.objects.filter(
                owner=self.request.user
            )
            form.fields["recipients"].queryset = Recipient.objects.filter(
                owner=self.request.user
            )
        return form


class NewsletterDeleteView(LoginRequiredMixin, ManagerOrOwnerMixin, DeleteView):
    model = Newsletter
    template_name = "newsletter_confirm_delete.html"  # Обновлено
    success_url = reverse_lazy("newsletter_list")


class AttemptListView(LoginRequiredMixin, ListView):
    model = Attempt
    template_name = "attempt_list.html"  # Обновлено

    def get_queryset(self):
        if self.request.user.is_manager():
            return Attempt.objects.all()
        return Attempt.objects.filter(newsletter__owner=self.request.user)


class AttemptDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Attempt
    template_name = "attempt_confirm_delete.html"  # Обновлено
    success_url = reverse_lazy("attempt_list")

    def test_func(self):
        attempt = self.get_object()
        return (
            self.request.user.is_manager()
            or attempt.newsletter.owner == self.request.user
        )

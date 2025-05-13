from django.urls import path
from .views import (
    RecipientListView,
    RecipientCreateView,
    RecipientUpdateView,
    RecipientDeleteView,
    MessageListView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView,
    NewsletterListView,
    NewsletterCreateView,
    NewsletterUpdateView,
    NewsletterDeleteView,
    AttemptListView,
    # Удаляем AttemptDeleteView, так как он не нужен
)
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="recipients/", permanent=False), name="home"),
    path("recipients/", RecipientListView.as_view(), name="recipient_list"),
    path("recipients/create/", RecipientCreateView.as_view(), name="recipient_create"),
    path(
        "recipients/<int:pk>/update/",
        RecipientUpdateView.as_view(),
        name="recipient_update",
    ),
    path(
        "recipients/<int:pk>/delete/",
        RecipientDeleteView.as_view(),
        name="recipient_delete",
    ),
    path("messages/", MessageListView.as_view(), name="message_list"),
    path("messages/create/", MessageCreateView.as_view(), name="message_create"),
    path(
        "messages/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"
    ),
    path(
        "messages/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"
    ),
    path("newsletters/", NewsletterListView.as_view(), name="newsletter_list"),
    path(
        "newsletters/create/", NewsletterCreateView.as_view(), name="newsletter_create"
    ),
    path(
        "newsletters/<int:pk>/update/",
        NewsletterUpdateView.as_view(),
        name="newsletter_update",
    ),
    path(
        "newsletters/<int:pk>/delete/",
        NewsletterDeleteView.as_view(),
        name="newsletter_delete",
    ),
    path("attempts/", AttemptListView.as_view(), name="attempt_list"),
    # Удаляем маршрут для attempts/<int:pk>/delete/
]

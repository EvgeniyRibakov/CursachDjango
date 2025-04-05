from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('newsletters.urls')),
    path('accounts/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
    path('mailing/', include('mailing_service.urls')),
]
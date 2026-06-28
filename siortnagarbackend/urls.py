"""
URL configuration for siortnagarbackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def api_root(request):
    """API root view with available endpoints."""
    return JsonResponse({
        "message": "Welcome to SIO RT Nagar API",
        "version": "1.0.0",
        "endpoints": {
            "public": {
                "home": "/api/home/",
                "office_bearers": "/api/about/office-bearers/",
                "activities": "/api/activities/",
                "books": "/api/library/books/",
                "events": "/api/events/",
                "event_detail": "/api/events/{id}/",
                "announcements": "/api/announcements/",
                "contact": "/api/contact/",
            },
            "admin": {
                "login": "/api/admin/login/",
                "token_refresh": "/api/admin/token/refresh/",
                "home": "/api/admin/home/",
                "office_bearers": "/api/admin/office-bearers/",
                "activities": "/api/admin/activities/",
                "books": "/api/admin/books/",
                "events": "/api/admin/events/",
                "event_photos": "/api/admin/event-photos/",
                "announcements": "/api/admin/announcements/",
                "contact": "/api/admin/contact/",
            }
        }
    })


urlpatterns = [
    path("", api_root, name="api-root"),
    path("django-admin/", admin.site.urls),
    path("api/", include("core.urls")),
]

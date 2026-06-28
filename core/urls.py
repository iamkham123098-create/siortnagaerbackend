from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    # Public views
    HomePagePublicView,
    OfficeBearerPublicListView,
    ActivityPublicListView,
    ActivityPublicDetailView,
    BookPublicListView,
    EventPublicListView,
    EventPublicDetailView,
    AnnouncementPublicListView,
    AnnouncementPublicDetailView,
    ContactInfoPublicView,
    # Admin viewsets
    HomePageAdminViewSet,
    OfficeBearerAdminViewSet,
    ActivityAdminViewSet,
    BookAdminViewSet,
    EventAdminViewSet,
    EventPhotoAdminViewSet,
    AnnouncementAdminViewSet,
    ContactInfoAdminViewSet,
)

# Admin router
admin_router = DefaultRouter()
admin_router.register(r"home", HomePageAdminViewSet, basename="admin-home")
admin_router.register(r"office-bearers", OfficeBearerAdminViewSet, basename="admin-office-bearers")
admin_router.register(r"activities", ActivityAdminViewSet, basename="admin-activities")
admin_router.register(r"books", BookAdminViewSet, basename="admin-books")
admin_router.register(r"events", EventAdminViewSet, basename="admin-events")
admin_router.register(r"event-photos", EventPhotoAdminViewSet, basename="admin-event-photos")
admin_router.register(r"announcements", AnnouncementAdminViewSet, basename="admin-announcements")
admin_router.register(r"contact", ContactInfoAdminViewSet, basename="admin-contact")

# Public URL patterns
public_urlpatterns = [
    path("home/", HomePagePublicView.as_view(), name="public-home"),
    path("about/office-bearers/", OfficeBearerPublicListView.as_view(), name="public-office-bearers"),
    path("activities/", ActivityPublicListView.as_view(), name="public-activities"),
    path("activities/<int:pk>/", ActivityPublicDetailView.as_view(), name="public-activity-detail"),
    path("library/books/", BookPublicListView.as_view(), name="public-books"),
    path("events/", EventPublicListView.as_view(), name="public-events"),
    path("events/<int:pk>/", EventPublicDetailView.as_view(), name="public-event-detail"),
    path("announcements/", AnnouncementPublicListView.as_view(), name="public-announcements"),
    path("announcements/<int:pk>/", AnnouncementPublicDetailView.as_view(), name="public-announcement-detail"),
    path("contact/", ContactInfoPublicView.as_view(), name="public-contact"),
]

# Admin URL patterns
admin_urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="admin-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="admin-token-refresh"),
    path("", include(admin_router.urls)),
]

# Combined URL patterns
urlpatterns = [
    path("", include(public_urlpatterns)),
    path("admin/", include(admin_urlpatterns)),
]

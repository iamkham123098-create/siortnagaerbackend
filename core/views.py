from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Case, When, Value, BooleanField
from django.utils import timezone
from datetime import timedelta

from .models import (
    HomePage, OfficeBearer, Activity, Book,
    Event, EventPhoto, Announcement, ContactInfo
)
from .filters import ActivityFilter, EventFilter, AnnouncementFilter
from .serializers import (
    # Public serializers
    HomePagePublicSerializer, OfficeBearerPublicSerializer,
    ActivityPublicSerializer, BookPublicSerializer,
    EventPublicSerializer, EventListPublicSerializer,
    EventPhotoPublicSerializer, AnnouncementPublicSerializer,
    ContactInfoPublicSerializer,
    # Admin serializers
    HomePageAdminSerializer, OfficeBearerAdminSerializer,
    ActivityAdminSerializer, BookAdminSerializer,
    EventAdminSerializer, EventPhotoAdminSerializer,
    AnnouncementAdminSerializer, ContactInfoAdminSerializer
)
from .permissions import IsAdminUser, IsAdminUserOrReadOnly


# ==================== HEALTH CHECK ====================

class HealthCheckView(generics.GenericAPIView):
    """Simple health check endpoint."""
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response({"status": "okay"}, status=status.HTTP_200_OK)


# ==================== PUBLIC VIEWS (Read-only) ====================

class HomePagePublicView(generics.RetrieveAPIView):
    """Public view for home page - returns single active home page."""
    serializer_class = HomePagePublicSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return HomePage.objects.filter(is_active=True).first()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response(
                {"detail": "Home page not configured."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class OfficeBearerPublicListView(generics.ListAPIView):
    """Public view for office bearers list."""
    serializer_class = OfficeBearerPublicSerializer
    permission_classes = [AllowAny]
    filter_backends = [OrderingFilter]
    ordering_fields = ["display_order", "name"]
    ordering = ["display_order"]

    def get_queryset(self):
        return OfficeBearer.objects.filter(is_active=True)


class ActivityPublicListView(generics.ListAPIView):
    """Public view for activities list with date filtering."""
    serializer_class = ActivityPublicSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ActivityFilter
    search_fields = ["title", "description"]
    ordering_fields = ["activity_date", "created_at"]
    ordering = ["-activity_date"]

    def get_queryset(self):
        return Activity.objects.filter(is_active=True)


class ActivityPublicDetailView(generics.RetrieveAPIView):
    """Public view for single activity detail."""
    serializer_class = ActivityPublicSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Activity.objects.filter(is_active=True)


class BookPublicListView(generics.ListAPIView):
    """Public view for books list with category filtering."""
    serializer_class = BookPublicSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category"]
    search_fields = ["title", "author", "description"]
    ordering_fields = ["title", "author", "created_at"]
    ordering = ["title"]

    def get_queryset(self):
        return Book.objects.filter(is_active=True)


class EventPublicListView(generics.ListAPIView):
    """Public view for events list with type and date filtering."""
    serializer_class = EventListPublicSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = EventFilter
    search_fields = ["title", "description", "location"]
    ordering_fields = ["event_date", "created_at"]
    ordering = ["-event_date"]

    def get_queryset(self):
        return Event.objects.filter(is_active=True)


class EventPublicDetailView(generics.RetrieveAPIView):
    """Public view for single event with photos."""
    serializer_class = EventPublicSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Event.objects.filter(is_active=True)


class AnnouncementPublicListView(generics.ListAPIView):
    """Public view for announcements list with date filtering."""
    serializer_class = AnnouncementPublicSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AnnouncementFilter
    search_fields = ["title", "content"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        # Annotate with computed_pinned for ordering (pinned within last 7 days)
        seven_days_ago = timezone.now() - timedelta(days=7)
        return Announcement.objects.filter(is_active=True).annotate(
            computed_pinned=Case(
                When(is_pinned=True, pinned_at__gte=seven_days_ago, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        ).order_by('-computed_pinned', '-created_at')


class AnnouncementPublicDetailView(generics.RetrieveAPIView):
    """Public view for single announcement detail."""
    serializer_class = AnnouncementPublicSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Announcement.objects.filter(is_active=True)


class ContactInfoPublicView(generics.RetrieveAPIView):
    """Public view for contact info - returns single active contact info."""
    serializer_class = ContactInfoPublicSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return ContactInfo.objects.filter(is_active=True).first()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response(
                {"detail": "Contact info not configured."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# ==================== ADMIN VIEWS (Full CRUD) ====================

class HomePageAdminViewSet(viewsets.ModelViewSet):
    """Admin viewset for home page - full CRUD."""
    serializer_class = HomePageAdminSerializer
    permission_classes = [IsAdminUser]
    queryset = HomePage.objects.all()

    def perform_destroy(self, instance):
        # Hard delete
        instance.delete()


class OfficeBearerAdminViewSet(viewsets.ModelViewSet):
    """Admin viewset for office bearers - full CRUD."""
    serializer_class = OfficeBearerAdminSerializer
    permission_classes = [IsAdminUser]
    queryset = OfficeBearer.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "position"]
    ordering_fields = ["display_order", "name", "created_at"]

    def perform_destroy(self, instance):
        # Hard delete
        instance.delete()


class ActivityAdminViewSet(viewsets.ModelViewSet):
    """Admin viewset for activities - full CRUD with date filtering."""
    serializer_class = ActivityAdminSerializer
    permission_classes = [IsAdminUser]
    queryset = Activity.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ActivityFilter
    search_fields = ["title", "description"]
    ordering_fields = ["activity_date", "created_at"]

    def perform_destroy(self, instance):
        # Hard delete
        instance.delete()


class BookAdminViewSet(viewsets.ModelViewSet):
    """Admin viewset for books - full CRUD."""
    serializer_class = BookAdminSerializer
    permission_classes = [IsAdminUser]
    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "is_active"]
    search_fields = ["title", "author", "description"]
    ordering_fields = ["title", "author", "created_at"]

    def perform_destroy(self, instance):
        # Hard delete
        instance.delete()


class EventAdminViewSet(viewsets.ModelViewSet):
    """Admin viewset for events - full CRUD with date filtering."""
    serializer_class = EventAdminSerializer
    permission_classes = [IsAdminUser]
    queryset = Event.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = EventFilter
    search_fields = ["title", "description", "location"]
    ordering_fields = ["event_date", "created_at"]

    def perform_destroy(self, instance):
        # Hard delete
        instance.delete()


class EventPhotoAdminViewSet(viewsets.ModelViewSet):
    """Admin viewset for event photos - full CRUD."""
    serializer_class = EventPhotoAdminSerializer
    permission_classes = [IsAdminUser]
    queryset = EventPhoto.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["event", "is_active"]

    def perform_destroy(self, instance):
        # Hard delete
        instance.delete()


class AnnouncementAdminViewSet(viewsets.ModelViewSet):
    """Admin viewset for announcements - full CRUD with date filtering."""
    serializer_class = AnnouncementAdminSerializer
    permission_classes = [IsAdminUser]
    queryset = Announcement.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AnnouncementFilter
    search_fields = ["title", "content"]
    ordering_fields = ["is_pinned", "created_at"]

    def perform_destroy(self, instance):
        # Hard delete
        instance.delete()


class ContactInfoAdminViewSet(viewsets.ModelViewSet):
    """Admin viewset for contact info - full CRUD."""
    serializer_class = ContactInfoAdminSerializer
    permission_classes = [IsAdminUser]
    queryset = ContactInfo.objects.all()

    def perform_destroy(self, instance):
        # Hard delete
        instance.delete()

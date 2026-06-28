from rest_framework import serializers
from .models import (
    HomePage, OfficeBearer, Activity, Book, 
    Event, EventPhoto, Announcement, ContactInfo
)
from .validators import validate_file_size


# ==================== PUBLIC SERIALIZERS (Read-only) ====================

class HomePagePublicSerializer(serializers.ModelSerializer):
    """Public serializer for home page - read only."""
    hero_banner_image = serializers.SerializerMethodField()

    class Meta:
        model = HomePage
        fields = [
            "id", "hero_banner_image", "hero_title", "hero_subtitle",
            "introduction", "vision", "mission", "cta_join_text", "cta_events_text"
        ]

    def get_hero_banner_image(self, obj):
        if obj.hero_banner_image:
            return obj.hero_banner_image.url
        return None


class OfficeBearerPublicSerializer(serializers.ModelSerializer):
    """Public serializer for office bearers - read only."""
    photo = serializers.SerializerMethodField()

    class Meta:
        model = OfficeBearer
        fields = ["id", "name", "position", "photo", "contact_number", "email", "display_order"]

    def get_photo(self, obj):
        if obj.photo:
            return obj.photo.url
        return None


class ActivityPublicSerializer(serializers.ModelSerializer):
    """Public serializer for activities - read only."""
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = ["id", "title", "description", "photo", "activity_date", "created_at"]

    def get_photo(self, obj):
        if obj.photo:
            return obj.photo.url
        return None


class BookPublicSerializer(serializers.ModelSerializer):
    """Public serializer for books - read only."""
    cover_image = serializers.SerializerMethodField()
    category_display = serializers.CharField(source="get_category_display", read_only=True)

    class Meta:
        model = Book
        fields = [
            "id", "title", "author", "category", "category_display",
            "cover_image", "drive_link", "description"
        ]

    def get_cover_image(self, obj):
        if obj.cover_image:
            return obj.cover_image.url
        return None


class EventPhotoPublicSerializer(serializers.ModelSerializer):
    """Public serializer for event photos."""
    photo = serializers.SerializerMethodField()

    class Meta:
        model = EventPhoto
        fields = ["id", "photo", "caption"]

    def get_photo(self, obj):
        if obj.photo:
            return obj.photo.url
        return None


class EventPublicSerializer(serializers.ModelSerializer):
    """Public serializer for events - read only."""
    photos = EventPhotoPublicSerializer(many=True, read_only=True)
    event_type_display = serializers.CharField(source="get_event_type_display", read_only=True)

    class Meta:
        model = Event
        fields = [
            "id", "title", "description", "event_date", "location",
            "event_type", "event_type_display", "photos", "created_at"
        ]


class EventListPublicSerializer(serializers.ModelSerializer):
    """Public serializer for events list - without photos for performance."""
    event_type_display = serializers.CharField(source="get_event_type_display", read_only=True)
    photo_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id", "title", "description", "event_date", "location",
            "event_type", "event_type_display", "photo_count", "created_at"
        ]

    def get_photo_count(self, obj):
        return obj.photos.filter(is_active=True).count()


class AnnouncementPublicSerializer(serializers.ModelSerializer):
    """Public serializer for announcements - read only."""
    is_pinned = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = ["id", "title", "content", "is_pinned", "pinned_at", "created_at"]

    def get_is_pinned(self, obj):
        """Return True only if pinned within last 7 days."""
        return obj.is_currently_pinned


class ContactInfoPublicSerializer(serializers.ModelSerializer):
    """Public serializer for contact info - read only."""

    class Meta:
        model = ContactInfo
        fields = [
            "id", "office_address", "google_maps_embed_url",
            "phone_numbers", "email", "social_media_links", "google_form_link"
        ]


# ==================== ADMIN SERIALIZERS (Full CRUD) ====================

class HomePageAdminSerializer(serializers.ModelSerializer):
    """Admin serializer for home page - full CRUD."""
    hero_banner_image_url = serializers.SerializerMethodField()

    class Meta:
        model = HomePage
        fields = "__all__"

    def get_hero_banner_image_url(self, obj):
        if obj.hero_banner_image:
            return obj.hero_banner_image.url
        return None

    def validate_hero_banner_image(self, value):
        if value:
            validate_file_size(value)
        return value


class OfficeBearerAdminSerializer(serializers.ModelSerializer):
    """Admin serializer for office bearers - full CRUD."""
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = OfficeBearer
        fields = "__all__"

    def get_photo_url(self, obj):
        if obj.photo:
            return obj.photo.url
        return None

    def validate_photo(self, value):
        if value:
            validate_file_size(value)
        return value


class ActivityAdminSerializer(serializers.ModelSerializer):
    """Admin serializer for activities - full CRUD."""
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = "__all__"

    def get_photo_url(self, obj):
        if obj.photo:
            return obj.photo.url
        return None

    def validate_photo(self, value):
        if value:
            validate_file_size(value)
        return value


class BookAdminSerializer(serializers.ModelSerializer):
    """Admin serializer for books - full CRUD."""
    cover_image_url = serializers.SerializerMethodField()
    category_display = serializers.CharField(source="get_category_display", read_only=True)

    class Meta:
        model = Book
        fields = "__all__"

    def get_cover_image_url(self, obj):
        if obj.cover_image:
            return obj.cover_image.url
        return None

    def validate_cover_image(self, value):
        if value:
            validate_file_size(value)
        return value


class EventPhotoAdminSerializer(serializers.ModelSerializer):
    """Admin serializer for event photos - full CRUD."""
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = EventPhoto
        fields = "__all__"

    def get_photo_url(self, obj):
        if obj.photo:
            return obj.photo.url
        return None

    def validate_photo(self, value):
        if value:
            validate_file_size(value)
        return value


class EventAdminSerializer(serializers.ModelSerializer):
    """Admin serializer for events - full CRUD."""
    photos = EventPhotoAdminSerializer(many=True, read_only=True)
    event_type_display = serializers.CharField(source="get_event_type_display", read_only=True)

    class Meta:
        model = Event
        fields = "__all__"


class AnnouncementAdminSerializer(serializers.ModelSerializer):
    """Admin serializer for announcements - full CRUD."""
    is_currently_pinned = serializers.BooleanField(read_only=True)

    class Meta:
        model = Announcement
        fields = "__all__"
        extra_kwargs = {
            'pinned_at': {'read_only': True}  # Auto-managed by model
        }


class ContactInfoAdminSerializer(serializers.ModelSerializer):
    """Admin serializer for contact info - full CRUD."""

    class Meta:
        model = ContactInfo
        fields = "__all__"

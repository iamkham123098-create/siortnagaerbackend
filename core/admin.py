from django.contrib import admin
from .models import (
    HomePage, OfficeBearer, Activity, Book,
    Event, EventPhoto, Announcement, ContactInfo
)


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ["id", "hero_title", "is_active", "created_at", "updated_at"]
    list_filter = ["is_active"]
    search_fields = ["hero_title", "introduction"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(OfficeBearer)
class OfficeBearerAdmin(admin.ModelAdmin):
    list_display = ["name", "position", "contact_number", "display_order", "is_active"]
    list_filter = ["is_active", "position"]
    search_fields = ["name", "position"]
    ordering = ["display_order", "name"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ["title", "activity_date", "is_active", "created_at"]
    list_filter = ["is_active", "activity_date"]
    search_fields = ["title", "description"]
    ordering = ["-activity_date"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "is_active", "created_at"]
    list_filter = ["is_active", "category"]
    search_fields = ["title", "author", "description"]
    ordering = ["title"]
    readonly_fields = ["created_at", "updated_at"]


class EventPhotoInline(admin.TabularInline):
    model = EventPhoto
    extra = 1
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "event_date", "event_type", "location", "is_active"]
    list_filter = ["is_active", "event_type", "event_date"]
    search_fields = ["title", "description", "location"]
    ordering = ["-event_date"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [EventPhotoInline]


@admin.register(EventPhoto)
class EventPhotoAdmin(admin.ModelAdmin):
    list_display = ["id", "event", "caption", "is_active", "created_at"]
    list_filter = ["is_active", "event"]
    search_fields = ["caption", "event__title"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ["title", "is_pinned", "is_active", "created_at"]
    list_filter = ["is_active", "is_pinned"]
    search_fields = ["title", "content"]
    ordering = ["-is_pinned", "-created_at"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "is_active", "created_at", "updated_at"]
    list_filter = ["is_active"]
    readonly_fields = ["created_at", "updated_at"]

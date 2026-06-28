from django.db import models
from cloudinary.models import CloudinaryField


class BaseModel(models.Model):
    """Abstract base model with common fields for soft delete and timestamps."""
    
    is_active = models.BooleanField(default=True, help_text="Soft delete flag")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class HomePage(BaseModel):
    """Home page content - singleton pattern (only one active record)."""
    
    hero_banner_image = CloudinaryField("hero_banner", blank=True, null=True)
    hero_title = models.CharField(max_length=200, blank=True)
    hero_subtitle = models.CharField(max_length=500, blank=True)
    introduction = models.TextField(blank=True, help_text="Introduction to SIO RT Nagar")
    vision = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    cta_join_text = models.CharField(max_length=100, default="Join Us", blank=True)
    cta_events_text = models.CharField(max_length=100, default="Upcoming Events", blank=True)

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Page"

    def __str__(self):
        return f"Home Page (Active: {self.is_active})"

    def save(self, *args, **kwargs):
        # Ensure only one active home page exists
        if self.is_active:
            HomePage.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class OfficeBearer(BaseModel):
    """Office bearers - name, position, photo, contact."""
    
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    photo = CloudinaryField("office_bearer_photos", blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    display_order = models.PositiveIntegerField(default=0, help_text="Order of display")

    class Meta:
        verbose_name = "Office Bearer"
        verbose_name_plural = "Office Bearers"
        ordering = ["display_order", "name"]

    def __str__(self):
        return f"{self.name} - {self.position}"


class Activity(BaseModel):
    """Weekly programs/activities."""
    
    title = models.CharField(max_length=300)
    description = models.TextField()
    photo = CloudinaryField("activity_photos", blank=True, null=True)
    activity_date = models.DateField()

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
        ordering = ["-activity_date"]

    def __str__(self):
        return f"{self.title} - {self.activity_date}"


class BookCategory(models.TextChoices):
    """Book category choices."""
    SIO_LITERATURE = "SIO_LITERATURE", "SIO Literature"
    CONTEMPORARY = "CONTEMPORARY", "Contemporary Literature"


class Book(BaseModel):
    """Digital library books with drive links."""
    
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=200)
    category = models.CharField(
        max_length=50,
        choices=BookCategory.choices,
        default=BookCategory.SIO_LITERATURE
    )
    cover_image = CloudinaryField("book_covers", blank=True, null=True)
    drive_link = models.URLField(help_text="Google Drive link to the PDF")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} by {self.author}"


class EventType(models.TextChoices):
    """Event type choices."""
    UPCOMING = "UPCOMING", "Upcoming"
    PAST = "PAST", "Past"


class Event(BaseModel):
    """Events - upcoming and past."""
    
    title = models.CharField(max_length=300)
    description = models.TextField()
    event_date = models.DateTimeField()
    location = models.CharField(max_length=300, blank=True)
    event_type = models.CharField(
        max_length=20,
        choices=EventType.choices,
        default=EventType.UPCOMING
    )

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ["-event_date"]

    def __str__(self):
        return f"{self.title} - {self.event_date.strftime('%Y-%m-%d')}"


class EventPhoto(BaseModel):
    """Photos for events."""
    
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="photos"
    )
    photo = CloudinaryField("event_photos")
    caption = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name = "Event Photo"
        verbose_name_plural = "Event Photos"

    def __str__(self):
        return f"Photo for {self.event.title}"


class Announcement(BaseModel):
    """Announcements/News."""
    
    title = models.CharField(max_length=300)
    content = models.TextField()
    is_pinned = models.BooleanField(default=False, help_text="Pin to top of list")
    pinned_at = models.DateTimeField(null=True, blank=True, help_text="When the announcement was pinned")

    class Meta:
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def is_currently_pinned(self):
        """Check if announcement is still pinned (within 7 days of pinning)."""
        from django.utils import timezone
        from datetime import timedelta
        
        if not self.is_pinned or not self.pinned_at:
            return False
        return timezone.now() - self.pinned_at <= timedelta(days=7)

    def save(self, *args, **kwargs):
        from django.utils import timezone
        
        # Always ensure pinned_at is set when is_pinned is True
        if self.is_pinned and not self.pinned_at:
            self.pinned_at = timezone.now()
        # Clear pinned_at when unpinned
        elif not self.is_pinned:
            self.pinned_at = None
        
        super().save(*args, **kwargs)


class ContactInfo(BaseModel):
    """Contact information - singleton pattern."""
    
    office_address = models.TextField()
    google_maps_embed_url = models.URLField(blank=True, help_text="Google Maps embed URL")
    phone_numbers = models.JSONField(default=list, help_text="List of phone numbers")
    email = models.EmailField()
    social_media_links = models.JSONField(
        default=dict,
        help_text="Dict of social media links: {'facebook': 'url', 'instagram': 'url', ...}"
    )
    google_form_link = models.URLField(blank=True, help_text="Google Form link for Join SIO")

    class Meta:
        verbose_name = "Contact Info"
        verbose_name_plural = "Contact Info"

    def __str__(self):
        return "Contact Information"

    def save(self, *args, **kwargs):
        # Ensure only one active contact info exists
        if self.is_active:
            ContactInfo.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

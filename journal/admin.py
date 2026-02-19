"""Admin model registrations for the journal app.

Register the Entry, GratitudeItem, and Quote models with
list displays and search fields for the Django admin site.
"""

from django.contrib import admin
from .models import Entry, GratitudeItem, Quote


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    """Admin options for Entry.

    Shows id, user, title, date and rating in the list view and allows
    filtering by date and mood.
    """

    list_display = ("id", "user", "title", "date", "mood_rating")
    list_filter = ("date", "mood")
    search_fields = ("title", "content", "user__username")


@admin.register(GratitudeItem)
class GratitudeItemAdmin(admin.ModelAdmin):
    """Admin options for GratitudeItem."""

    list_display = ("id", "entry", "item_text")
    search_fields = ("item_text",)


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    """Admin options for Quote."""

    list_display = ("id", "author")
    search_fields = ("text", "author")

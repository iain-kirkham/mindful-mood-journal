from django.contrib import admin
from .models import Entry, GratitudeItem, Quote


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "date", "mood_rating")
    list_filter = ("date", "mood")
    search_fields = ("title", "content", "user__username")



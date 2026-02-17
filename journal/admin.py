from django.contrib import admin
from .models import Entry, GratitudeItem, Quote


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "date", "mood_rating")
    list_filter = ("date", "mood")
    search_fields = ("title", "content", "user__username")

@admin.register(GratitudeItem)
class GratitudeItemAdmin(admin.ModelAdmin):
    list_display = ("id", "entry", "item_text")
    search_fields = ("item_text",)

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("id", "author")
    search_fields = ("text", "author")
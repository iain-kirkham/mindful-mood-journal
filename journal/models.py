"""Data models for the MoodJournal application.

This module defines the main persistent objects used by the app:
- Entry: a user's journal entry containing mood and rating
- GratitudeItem: short text items attached to an Entry
- Quote: optional inspirational quote shown on the home page
"""

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


MOOD_CHOICES = [
    ("happy", "Happy"),
    ("anxious", "Anxious"),
    ("sad", "Sad"),
    ("neutral", "Neutral"),
    ("excited", "Excited"),
    ("frustrated", "Frustrated"),
    ("calm", "Calm"),
    ("stressed", "Stressed"),
]


class Entry(models.Model):
    """A journal entry created by a user.

    Fields:
        user (ForeignKey): the author of the entry
        date (DateTimeField): when the entry was written
        mood (CharField): one of `MOOD_CHOICES`
        mood_rating (IntegerField): rating between 1 and 5
        title (CharField): short title of the entry
        content (TextField): full text of the entry
        created_at (DateTimeField): DB timestamp when the row was created
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="entries",
    )
    date = models.DateTimeField()
    mood = models.CharField(max_length=50, choices=MOOD_CHOICES)
    mood_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user} - {self.title} ({self.date.date()})"


class GratitudeItem(models.Model):
    """A short gratitude item associated with an Entry.

    Stored as a small text field and linked to its parent entry via FK.
    """

    entry = models.ForeignKey(
        Entry, on_delete=models.CASCADE, related_name="gratitude_items"
    )
    item_text = models.CharField(max_length=255)

    def __str__(self):
        return self.item_text


class Quote(models.Model):
    """A short inspirational quote displayed on the home page.

    The author field is optional and may be blank.
    """

    text = models.TextField()
    author = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.text[:50]}{'...' if len(self.text) > 50 else ''} - {self.author}"

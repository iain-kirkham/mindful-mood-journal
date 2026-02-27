"""Data models for the MoodJournal application.

This module defines the main persistent objects used by the app:
- Entry: a user's journal entry containing mood and rating
- GratitudeItem: short text items attached to an Entry
- Quote: optional inspirational quote shown on the home page

database-level CHECK constraints validate at the DB layer. The constraints are:
- Entry: `mood_rating` must be between 1 and 5; `mood` must be one of
    the defined `MOOD_CHOICES`; `title` and `content` must not be empty.
- GratitudeItem: `item_text` must not be empty.
- Quote: `text` must not be empty.
"""

from django.db import models
from django.db.models import Q
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

    Database constraints (enforced at the DB level):
        - `mood_rating` must be between 1 and 5
        - `mood` must be one of `MOOD_CHOICES`
        - `title` must not be an empty string
        - `content` must not be an empty string
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
        constraints = [
            models.CheckConstraint(
                check=Q(mood_rating__gte=1) & Q(mood_rating__lte=5),
                name="entry_mood_rating_1_to_5",
            ),
            models.CheckConstraint(
                check=Q(mood__in=[choice[0] for choice in MOOD_CHOICES]),
                name="entry_mood_valid_choice",
            ),
            models.CheckConstraint(
                check=~Q(title=""),
                name="entry_title_not_empty",
            ),
            models.CheckConstraint(
                check=~Q(content=""),
                name="entry_content_not_empty",
            ),
        ]

    def __str__(self):
        return f"{self.user} - {self.title} ({self.date.date()})"


class GratitudeItem(models.Model):
    """A short gratitude item associated with an Entry.

    Stored as a small text field and linked to its parent entry via FK.

    Database constraints:
        - `item_text` must not be an empty string
    """

    entry = models.ForeignKey(
        Entry, on_delete=models.CASCADE, related_name="gratitude_items"
    )
    item_text = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~Q(item_text=""),
                name="gratitudeitem_text_not_empty",
            ),
        ]

    def __str__(self):
        return self.item_text


class Quote(models.Model):
    """A short inspirational quote displayed on the home page.

    The author field is optional and may be blank.

    Database constraints:
        - `text` must not be an empty string
    """

    text = models.TextField()
    author = models.CharField(max_length=200, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~Q(text=""),
                name="quote_text_not_empty",
            ),
        ]

    def __str__(self):
        preview = self.text[:50]
        ellipsis = "..." if len(self.text) > 50 else ""
        return f"{preview}{ellipsis} - {self.author}"

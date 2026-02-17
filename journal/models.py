from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Entry(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="entries",
    )
    date = models.DateTimeField()
    mood = models.CharField(max_length=50)
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
    entry = models.ForeignKey(
        Entry, on_delete=models.CASCADE, related_name="gratitude_items"
    )
    item_text = models.CharField(max_length=255)

    def __str__(self):
        return self.item_text

class Quote(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.text[:50]}{'...' if len(self.text) > 50 else ''} - {self.author}"
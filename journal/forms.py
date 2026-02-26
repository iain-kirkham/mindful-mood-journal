"""Forms for the journal app.

Provides EntryForm for creating/editing journal entries and a compact
GratitudeItemForm plus two formsets for creating and editing gratitude
items attached to an Entry.
"""

from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone
from .models import Entry, GratitudeItem, MOOD_CHOICES

MAX_FUTURE_DAYS = 1  # allow up to 1 day ahead to accommodate timezone shifts


MOOD_RATING_CHOICES = [
    (1, "1 - Very Poor"),
    (2, "2 - Poor"),
    (3, "3 - Neutral"),
    (4, "4 - Good"),
    (5, "5 - Excellent"),
]


class EntryForm(forms.ModelForm):
    """ModelForm for Entry used by create and update views.

    The date field is rendered as a datetime-local input and defaults to
    the current time when creating a new entry.
    """

    class Meta:
        model = Entry
        fields = ["date", "mood", "mood_rating", "title", "content"]
        widgets = {
            "date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "mood": forms.Select(choices=MOOD_CHOICES),
            "mood_rating": forms.Select(choices=MOOD_RATING_CHOICES),
            "title": forms.TextInput(attrs={"placeholder": "Journal title"}),
            "content": forms.Textarea(attrs={"rows": 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Default date to now for new instances to ease entry creation.
        if not self.instance.pk:
            self.fields["date"].initial = timezone.now()

    def clean_title(self):
        title = self.cleaned_data.get("title", "").strip()
        if not title:
            raise forms.ValidationError("Title cannot be blank.")
        return title

    def clean_content(self):
        content = self.cleaned_data.get("content", "").strip()
        if not content:
            raise forms.ValidationError("Content cannot be blank.")
        return content

    def clean_mood_rating(self):
        rating = self.cleaned_data.get("mood_rating")
        if rating is not None and not (1 <= rating <= 5):
            raise forms.ValidationError("Mood rating must be between 1 and 5.")
        return rating

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date is None:
            raise forms.ValidationError("Please enter a valid date and time.")
        if date > timezone.now() + timezone.timedelta(days=MAX_FUTURE_DAYS):
            raise forms.ValidationError(
                "Entry date cannot be more than a day in the future."
            )
        return date


class GratitudeItemForm(forms.ModelForm):
    """Single gratitude item form used in create/edit formsets.

    Hides the visible label for compact inline rendering and keeps an
    `aria-label` for accessibility.  Gratitude items are entirely optional;
    blank rows in the formset are silently ignored.
    """

    class Meta:
        model = GratitudeItem
        fields = ("item_text",)
        widgets = {
            "item_text": forms.TextInput(
                attrs={"aria-label": "Thing you're grateful for"}
            )
        }
        labels = {"item_text": ""}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mark as not required so that empty rows in the formset are skipped.
        self.fields["item_text"].required = False

    def clean_item_text(self):
        text = self.cleaned_data.get("item_text", "").strip()
        # Treat whitespace-only input as empty if changed, require non-empty.
        if self.has_changed() and not text:
            raise forms.ValidationError(
                "Gratitude item cannot be blank. Leave the field empty to skip it."
            )
        return text


GratitudeFormSet = inlineformset_factory(
    Entry, GratitudeItem, form=GratitudeItemForm, extra=3, can_delete=False
)

GratitudeEditFormSet = inlineformset_factory(
    Entry, GratitudeItem, form=GratitudeItemForm, extra=0, can_delete=False
)


def make_gratitude_edit_formset(extra=0):
    """Return a GratitudeItem edit formset class with a dynamic extra count.

    Used by the edit view to ensure the minimum visible boxes is always 3
    regardless of how many gratitude items the entry already has.
    """
    return inlineformset_factory(
        Entry, GratitudeItem, form=GratitudeItemForm, extra=extra, can_delete=False
    )

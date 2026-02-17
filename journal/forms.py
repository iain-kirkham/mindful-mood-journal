from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone
from .models import Entry, GratitudeItem, MOOD_CHOICES


MOOD_RATING_CHOICES = [
    (1, "1 - Very Poor"),
    (2, "2 - Poor"),
    (3, "3 - Neutral"),
    (4, "4 - Good"),
    (5, "5 - Excellent"),
]


class EntryForm(forms.ModelForm):
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
        if not self.instance.pk:
            self.fields["date"].initial = timezone.now()


class GratitudeItemForm(forms.ModelForm):
    class Meta:
        model = GratitudeItem
        fields = ("item_text",)
        widgets = {
            "item_text": forms.TextInput(
                attrs={"aria-label": "Thing you're grateful for"}
            )
        }
        labels = {
            "item_text": ""
        }


GratitudeFormSet = inlineformset_factory(
    Entry, GratitudeItem, form=GratitudeItemForm, extra=3, can_delete=False
)

GratitudeEditFormSet = inlineformset_factory(
    Entry, GratitudeItem, form=GratitudeItemForm, extra=0, can_delete=False
)

"""Tests for journal forms: EntryForm, GratitudeItemForm, and formsets.

This module tests form initialisation, field configuration, widget types,
form field choices, and formset behavior to ensure forms render and validate correctly.
"""

from datetime import datetime, timedelta

from django.test import TestCase
from django.utils import timezone
from django.forms import DateTimeInput, Select
from django.contrib.auth import get_user_model

from journal.forms import (
    EntryForm,
    GratitudeFormSet,
    GratitudeEditFormSet,
    MOOD_RATING_CHOICES,
)
from journal.models import MOOD_CHOICES, Entry


class EntryFormTests(TestCase):
    """Tests for EntryForm: initialisation, widgets, and field configuration."""

    def test_initial_date_for_new_entry(self):
        """Verify that the date field defaults to the current time for new entries."""
        form = EntryForm()
        initial = form.fields["date"].initial
        self.assertIsNotNone(initial)
        self.assertIsInstance(initial, datetime)
        self.assertLess(abs(timezone.now() - initial), timedelta(seconds=5))

    def test_widget_and_choices(self):
        """Verify form field widgets and choice options are configured correctly.

        Checks that:
        - Date field uses DateTimeInput widget
        - Mood field has correct mood choices (handling Django's optional empty choice)
        - Mood rating field uses Select widget with correct 1-5 rating choices
        """
        form = EntryForm()
        self.assertIsInstance(form.fields["date"].widget, DateTimeInput)
        mood_choices = form.fields["mood"].choices
        # Some Django versions include an initial empty choice; allow that.
        if mood_choices and mood_choices[0][0] == "":
            self.assertEqual(mood_choices[1:], MOOD_CHOICES)
        else:
            self.assertEqual(mood_choices, MOOD_CHOICES)
        # `mood_rating` is an IntegerField with a Select widget; check widget choices
        self.assertIsInstance(form.fields["mood_rating"].widget, Select)
        self.assertEqual(form.fields["mood_rating"].widget.choices, MOOD_RATING_CHOICES)


class GratitudeFormsetTests(TestCase):
    """Tests for gratitude formsets: form count and configuration."""

    def setUp(self):
        """Create a test user and entry for formset tests."""
        User = get_user_model()
        self.user = User.objects.create_user(username="tester", password="pass")
        self.entry = Entry.objects.create(
            user=self.user,
            date=timezone.now(),
            mood=MOOD_CHOICES[0][0],
            mood_rating=3,
            title="Test",
            content="Test content",
        )

    def test_gratitude_formset_extra(self):
        """Verify GratitudeFormSet provides 3 extra blank forms for entry creation.

        The formset is used during entry creation to allow users to add 3 gratitude items.
        """
        formset = GratitudeFormSet(instance=self.entry)
        self.assertEqual(len(formset.forms), 3)

    def test_gratitude_edit_formset_no_extra(self):
        """Verify GratitudeEditFormSet provides no extra blank forms during editing.

        The edit formset shows only existing gratitude items without extra blanks,
        preventing unintended item creation during an edit.
        """
        formset = GratitudeEditFormSet(instance=self.entry)
        self.assertEqual(len(formset.forms), 0)

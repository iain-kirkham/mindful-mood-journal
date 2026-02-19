"""Unit tests for journal models: Entry, GratitudeItem, and Quote.

Tests cover string representations, field validators, Meta ordering,
and cascade-delete behaviour.
"""

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from journal.models import Entry, GratitudeItem, Quote

User = get_user_model()


def make_user(username="testuser", password="testpassword"):
    """Helper: create and return a test user."""
    return User.objects.create_user(username=username, password=password)


def make_entry(user, **kwargs):
    """Helper: create and return an Entry."""
    defaults = {
        "date": timezone.now(),
        "mood": "happy",
        "mood_rating": 3,
        "title": "Test Entry",
        "content": "This is a test entry.",
    }
    defaults.update(kwargs)
    return Entry.objects.create(user=user, **defaults)


class EntryStrTests(TestCase):
    """Tests for Entry.__str__."""

    def setUp(self):
        self.user = make_user()
        self.entry = make_entry(self.user, title="My Day")

    def test_str_contains_username(self):
        self.assertIn(str(self.user), str(self.entry))

    def test_str_contains_title(self):
        self.assertIn("My Day", str(self.entry))

    def test_str_contains_date(self):
        expected_date = str(self.entry.date.date())
        self.assertIn(expected_date, str(self.entry))

    def test_str_format(self):
        expected = f"{self.user} - My Day ({self.entry.date.date()})"
        self.assertEqual(str(self.entry), expected)


class EntryOrderingTests(TestCase):
    """Entry rows should be returned newest-date-first by default."""

    def setUp(self):
        self.user = make_user()
        now = timezone.now()
        self.older = make_entry(
            self.user, title="Older", date=now - timezone.timedelta(days=2)
        )
        self.newer = make_entry(self.user, title="Newer", date=now)

    def test_default_ordering_newest_first(self):
        entries = list(Entry.objects.all())
        self.assertEqual(entries[0], self.newer)
        self.assertEqual(entries[1], self.older)


class EntryMoodRatingValidatorTests(TestCase):
    """mood_rating must be between 1 and 5 (inclusive)."""

    def setUp(self):
        self.user = make_user()

    def _entry_with_rating(self, rating):
        entry = Entry(
            user=self.user,
            date=timezone.now(),
            mood="happy",
            mood_rating=rating,
            title="T",
            content="C",
        )
        entry.full_clean()  # triggers validators
        return entry

    def test_rating_1_is_valid(self):
        try:
            self._entry_with_rating(1)
        except ValidationError:
            self.fail("mood_rating=1 raised ValidationError unexpectedly.")

    def test_rating_5_is_valid(self):
        try:
            self._entry_with_rating(5)
        except ValidationError:
            self.fail("mood_rating=5 raised ValidationError unexpectedly.")

    def test_rating_0_is_invalid(self):
        with self.assertRaises(ValidationError):
            self._entry_with_rating(0)

    def test_rating_6_is_invalid(self):
        with self.assertRaises(ValidationError):
            self._entry_with_rating(6)


class EntryCascadeDeleteTests(TestCase):
    """Deleting a user should cascade and remove their entries."""

    def test_entry_deleted_when_user_deleted(self):
        user = make_user()
        make_entry(user)
        self.assertEqual(Entry.objects.count(), 1)
        user.delete()
        self.assertEqual(Entry.objects.count(), 0)


class GratitudeItemStrTests(TestCase):
    """Tests for GratitudeItem.__str__."""

    def setUp(self):
        user = make_user()
        entry = make_entry(user)
        self.item = GratitudeItem.objects.create(entry=entry, item_text="Sunshine")

    def test_str_equals_item_text(self):
        self.assertEqual(str(self.item), "Sunshine")


class GratitudeItemCascadeDeleteTests(TestCase):
    """GratitudeItems should be deleted when their parent Entry is deleted."""

    def test_items_deleted_when_entry_deleted(self):
        user = make_user()
        entry = make_entry(user)
        GratitudeItem.objects.create(entry=entry, item_text="Friends")
        GratitudeItem.objects.create(entry=entry, item_text="Coffee")
        self.assertEqual(GratitudeItem.objects.count(), 2)
        entry.delete()
        self.assertEqual(GratitudeItem.objects.count(), 0)

    def test_items_not_deleted_when_unrelated_entry_deleted(self):
        user = make_user()
        entry1 = make_entry(user, title="Entry 1")
        entry2 = make_entry(user, title="Entry 2")
        GratitudeItem.objects.create(entry=entry1, item_text="Keep this")
        GratitudeItem.objects.create(entry=entry2, item_text="Delete this")
        entry2.delete()
        self.assertEqual(GratitudeItem.objects.count(), 1)
        self.assertEqual(GratitudeItem.objects.get().item_text, "Keep this")


class QuoteStrTests(TestCase):
    """Tests for Quote.__str__."""

    def test_short_text_not_truncated(self):
        quote = Quote(text="Short text.", author="Someone")
        self.assertEqual(str(quote), "Short text. - Someone")

    def test_long_text_truncated_at_50_chars(self):
        long_text = "A" * 60
        quote = Quote(text=long_text, author="Author")
        result = str(quote)
        self.assertTrue(result.startswith("A" * 50 + "..."))

    def test_text_exactly_50_chars_not_truncated(self):
        text = "B" * 50
        quote = Quote(text=text, author="Author")
        result = str(quote)
        self.assertNotIn("...", result)
        self.assertIn(text, result)

    def test_blank_author(self):
        quote = Quote(text="Some thought.", author="")
        result = str(quote)
        self.assertEqual(result, "Some thought. - ")

    def test_str_contains_author(self):
        quote = Quote(text="Wisdom.", author="Plato")
        self.assertIn("Plato", str(quote))

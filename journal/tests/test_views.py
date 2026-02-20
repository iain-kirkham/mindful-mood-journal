"""Unit tests for journal views.

Covers every view in journal/views.py across three dimensions:
  - Authentication: unauthenticated users are redirected to login.
  - Authorisation: users cannot see or modify another user's entries.
  - Behaviour: GET/POST happy-paths, validation failures, messages, redirects.

Views under test
~~~~~~~~~~~~~~~~
HomeView            GET /
EntryListView       GET /entries/
EntryDetailView     GET /entries/<pk>/
EntryCreateView     GET|POST /entries/create/
EntryUpdateView     GET|POST /entries/<pk>/edit/
EntryDeleteView     GET|POST /entries/<pk>/delete/
create_success      GET /entries/create/success/
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from journal.models import Entry, GratitudeItem, Quote

User = get_user_model()

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

LOGIN_URL = "/accounts/login/"


def make_user(username="alice", password="testpassword123"):
    return User.objects.create_user(username=username, password=password)


def make_entry(user, **kwargs):
    defaults = {
        "date": timezone.now(),
        "mood": "happy",
        "mood_rating": 3,
        "title": "My Entry",
        "content": "Some content.",
    }
    defaults.update(kwargs)
    return Entry.objects.create(user=user, **defaults)


# Management-form fields required by GratitudeFormSet (prefix = gratitude_items)
def gratitude_management_form(total=3, initial=0):
    return {
        "gratitude_items-TOTAL_FORMS": total,
        "gratitude_items-INITIAL_FORMS": initial,
        "gratitude_items-MIN_NUM_FORMS": 0,
        "gratitude_items-MAX_NUM_FORMS": 1000,
    }


def valid_entry_post(**overrides):
    data = {
        "date": "2026-01-15T10:00",
        "mood": "calm",
        "mood_rating": 4,
        "title": "Good Day",
        "content": "Felt pretty good.",
        **gratitude_management_form(),
        "gratitude_items-0-item_text": "Sunshine",
        "gratitude_items-1-item_text": "",
        "gratitude_items-2-item_text": "",
    }
    data.update(overrides)
    return data


# ---------------------------------------------------------------------------
# HomeView  GET /
# ---------------------------------------------------------------------------


class HomeViewTests(TestCase):
    def test_get_returns_200(self):
        response = self.client.get(reverse("journal:home"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("journal:home"))
        self.assertTemplateUsed(response, "journal/home.html")

    def test_quote_key_in_context(self):
        response = self.client.get(reverse("journal:home"))
        self.assertIn("quote", response.context)

    def test_quote_context_returns_quote_object_when_one_exists(self):
        Quote.objects.create(text="Test wisdom.", author="Tester")
        response = self.client.get(reverse("journal:home"))
        self.assertIsNotNone(response.context["quote"])

    def test_quote_context_is_none_when_no_quotes(self):
        Quote.objects.all().delete()
        response = self.client.get(reverse("journal:home"))
        self.assertIsNone(response.context["quote"])

    def test_accessible_without_login(self):
        """Home page must be publicly accessible."""
        response = self.client.get(reverse("journal:home"))
        self.assertNotEqual(response.status_code, 302)


# ---------------------------------------------------------------------------
# EntryListView  GET /entries/
# ---------------------------------------------------------------------------


class EntryListViewTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.other = make_user(username="bob")
        self.url = reverse("journal:entry_list")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(
            response, f"{LOGIN_URL}?next={self.url}", fetch_redirect_response=False
        )

    def test_get_returns_200(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "journal/entry_list.html")

    def test_only_shows_own_entries(self):
        own = make_entry(self.user, title="Mine")
        make_entry(self.other, title="Not mine")
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        entries = list(response.context["entries"])
        self.assertIn(own, entries)
        self.assertEqual(len(entries), 1)

    def test_empty_list_for_new_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(len(response.context["entries"]), 0)

    def test_search_by_title(self):
        make_entry(self.user, title="Rainy Monday")
        make_entry(self.user, title="Sunny Friday")
        self.client.force_login(self.user)
        response = self.client.get(self.url, {"search": "Rainy"})
        entries = list(response.context["entries"])
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].title, "Rainy Monday")

    def test_search_by_content(self):
        make_entry(self.user, content="I learned Django today")
        make_entry(self.user, content="Went for a walk")
        self.client.force_login(self.user)
        response = self.client.get(self.url, {"search": "Django"})
        self.assertEqual(len(response.context["entries"]), 1)

    def test_search_by_mood(self):
        make_entry(self.user, mood="excited")
        make_entry(self.user, mood="sad")
        self.client.force_login(self.user)
        response = self.client.get(self.url, {"search": "excited"})
        entries = list(response.context["entries"])
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].mood, "excited")

    def test_search_by_gratitude_item(self):
        entry = make_entry(self.user)
        GratitudeItem.objects.create(entry=entry, item_text="Coffee")
        make_entry(self.user, title="Other")  # no gratitude items
        self.client.force_login(self.user)
        response = self.client.get(self.url, {"search": "Coffee"})
        self.assertEqual(len(response.context["entries"]), 1)

    def test_search_no_match_returns_empty(self):
        make_entry(self.user, title="Normal Entry")
        self.client.force_login(self.user)
        response = self.client.get(self.url, {"search": "zzznomatch"})
        self.assertEqual(len(response.context["entries"]), 0)

    def test_search_term_present_in_context(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url, {"search": "hello"})
        self.assertEqual(response.context["search"], "hello")

    def test_search_defaults_to_empty_string(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.context["search"], "")


# ---------------------------------------------------------------------------
# EntryDetailView  GET /entries/<pk>/
# ---------------------------------------------------------------------------


class EntryDetailViewTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.other = make_user(username="carol")
        self.entry = make_entry(self.user)
        self.url = reverse("journal:entry_detail", kwargs={"pk": self.entry.pk})

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(
            response, f"{LOGIN_URL}?next={self.url}", fetch_redirect_response=False
        )

    def test_get_returns_200(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "journal/entry_detail.html")

    def test_entry_in_context(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.context["entry"], self.entry)

    def test_404_for_other_users_entry(self):
        self.client.force_login(self.other)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)


# ---------------------------------------------------------------------------
# EntryCreateView  GET|POST /entries/create/
# ---------------------------------------------------------------------------


class EntryCreateViewGetTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.url = reverse("journal:entry_create")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(
            response, f"{LOGIN_URL}?next={self.url}", fetch_redirect_response=False
        )

    def test_get_returns_200(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "journal/entry_form.html")

    def test_form_and_formset_in_context(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertIn("form", response.context)
        self.assertIn("formset", response.context)


class EntryCreateViewPostTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.url = reverse("journal:entry_create")
        self.client.force_login(self.user)

    def test_valid_post_creates_entry(self):
        self.client.post(self.url, valid_entry_post())
        self.assertEqual(Entry.objects.filter(user=self.user).count(), 1)

    def test_valid_post_assigns_entry_to_current_user(self):
        self.client.post(self.url, valid_entry_post())
        entry = Entry.objects.get(user=self.user)
        self.assertEqual(entry.user, self.user)

    def test_valid_post_saves_gratitude_items(self):
        data = valid_entry_post(**{"gratitude_items-0-item_text": "Health"})
        self.client.post(self.url, data)
        entry = Entry.objects.get(user=self.user)
        self.assertTrue(entry.gratitude_items.filter(item_text="Health").exists())

    def test_valid_post_redirects_to_success(self):
        response = self.client.post(self.url, valid_entry_post())
        self.assertRedirects(response, reverse("journal:entry_create_success"))

    def test_valid_post_sets_success_message(self):
        self.client.post(self.url, valid_entry_post(title="Sunny Day"))
        messages = list(
            self.client.get(
                reverse("journal:entry_create_success")
            ).wsgi_request._messages
        )
        # Message is consumed on the next request; check via follow
        response = self.client.post(
            self.url, valid_entry_post(title="Day Two"), follow=True
        )
        msgs = [str(m) for m in response.context["messages"]]
        self.assertTrue(any("Day Two" in m for m in msgs))

    def test_invalid_post_does_not_create_entry(self):
        bad_data = valid_entry_post(title="")  # title is required
        self.client.post(self.url, bad_data)
        self.assertEqual(Entry.objects.filter(user=self.user).count(), 0)

    def test_invalid_post_returns_200(self):
        bad_data = valid_entry_post(title="")
        response = self.client.post(self.url, bad_data)
        self.assertEqual(response.status_code, 200)

    def test_invalid_post_rerenders_form_with_errors(self):
        bad_data = valid_entry_post(mood_rating=99)  # out-of-range rating
        response = self.client.post(self.url, bad_data)
        self.assertTemplateUsed(response, "journal/entry_form.html")
        self.assertTrue(response.context["form"].errors)


# ---------------------------------------------------------------------------
# EntryUpdateView  GET|POST /entries/<pk>/edit/
# ---------------------------------------------------------------------------


class EntryUpdateViewGetTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.other = make_user(username="dave")
        self.entry = make_entry(self.user, title="Original Title")
        self.url = reverse("journal:entry_update", kwargs={"pk": self.entry.pk})

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(
            response, f"{LOGIN_URL}?next={self.url}", fetch_redirect_response=False
        )

    def test_get_returns_200(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "journal/entry_form.html")

    def test_form_prefilled_with_entry_data(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.context["form"].instance, self.entry)

    def test_is_edit_flag_in_context(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertTrue(response.context.get("is_edit"))

    def test_404_for_other_users_entry(self):
        self.client.force_login(self.other)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)


class EntryUpdateViewPostTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.other = make_user(username="eve")
        self.entry = make_entry(self.user, title="Old Title")
        self.url = reverse("journal:entry_update", kwargs={"pk": self.entry.pk})
        self.client.force_login(self.user)

    def _edit_formset_data(self):
        """Management form for GratitudeEditFormSet with 0 existing items."""
        return {
            "gratitude_items-TOTAL_FORMS": 1,
            "gratitude_items-INITIAL_FORMS": 0,
            "gratitude_items-MIN_NUM_FORMS": 0,
            "gratitude_items-MAX_NUM_FORMS": 1000,
            "gratitude_items-0-item_text": "",
        }

    def valid_update_post(self, **overrides):
        data = {
            "date": "2026-02-01T08:00",
            "mood": "neutral",
            "mood_rating": 2,
            "title": "Updated Title",
            "content": "Updated content.",
            **self._edit_formset_data(),
        }
        data.update(overrides)
        return data

    def test_valid_post_updates_entry_title(self):
        self.client.post(self.url, self.valid_update_post(title="New Title"))
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.title, "New Title")

    def test_valid_post_redirects_to_detail(self):
        response = self.client.post(self.url, self.valid_update_post())
        self.assertRedirects(
            response, reverse("journal:entry_detail", kwargs={"pk": self.entry.pk})
        )

    def test_valid_post_sets_success_message(self):
        response = self.client.post(
            self.url, self.valid_update_post(title="Fresh Title"), follow=True
        )
        msgs = [str(m) for m in response.context["messages"]]
        self.assertTrue(any("Fresh Title" in m for m in msgs))

    def test_invalid_post_returns_200(self):
        bad = self.valid_update_post(title="")
        response = self.client.post(self.url, bad)
        self.assertEqual(response.status_code, 200)

    def test_invalid_post_does_not_update_entry(self):
        self.client.post(self.url, self.valid_update_post(title=""))
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.title, "Old Title")

    def test_404_for_other_users_entry(self):
        self.client.force_login(self.other)
        response = self.client.post(self.url, self.valid_update_post())
        self.assertEqual(response.status_code, 404)


# ---------------------------------------------------------------------------
# EntryDeleteView  GET|POST /entries/<pk>/delete/
# ---------------------------------------------------------------------------


class EntryDeleteViewTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.other = make_user(username="frank")
        self.entry = make_entry(self.user)
        self.url = reverse("journal:entry_delete", kwargs={"pk": self.entry.pk})

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(
            response, f"{LOGIN_URL}?next={self.url}", fetch_redirect_response=False
        )

    def test_get_returns_200(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "journal/entry_confirm_delete.html")

    def test_post_deletes_entry(self):
        self.client.force_login(self.user)
        self.client.post(self.url)
        self.assertFalse(Entry.objects.filter(pk=self.entry.pk).exists())

    def test_post_redirects_to_list(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("journal:entry_list"))

    def test_post_sets_success_message(self):
        self.entry.title = "Day One"
        self.entry.save()
        self.client.force_login(self.user)
        response = self.client.post(self.url, follow=True)
        msgs = [str(m) for m in response.context["messages"]]
        self.assertTrue(any("Day One" in m for m in msgs))

    def test_get_404_for_other_users_entry(self):
        self.client.force_login(self.other)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_post_404_for_other_users_entry(self):
        self.client.force_login(self.other)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Entry.objects.filter(pk=self.entry.pk).exists())


# ---------------------------------------------------------------------------
# entry_create_success  GET /entries/create/success/
# ---------------------------------------------------------------------------


class EntryCreateSuccessViewTests(TestCase):
    def setUp(self):
        self.url = reverse("journal:entry_create_success")

    def test_get_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "journal/create_success.html")

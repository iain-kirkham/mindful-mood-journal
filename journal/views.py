"""Views for the journal application.

Provides CRUD operations for journal entries along with search functionality,
gratitude item management via inline formsets, and a home page with random quotes.

All entry-related views require user authentication and ensure users can only
access their own entries.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, DetailView, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db import transaction
from django.contrib import messages

from .forms import (
    EntryForm,
    GratitudeEditFormSet,
    GratitudeFormSet,
    make_gratitude_edit_formset,
)
from .models import Entry, Quote


class EntryCreateView(LoginRequiredMixin, View):
    """View for creating a new journal entry with optional gratitude items.

    GET: Display empty entry form and gratitude formset.
    POST: Validate and save entry with associated gratitude items in a transaction.

    Uses an atomic transaction to ensure the entry is only saved if both the
    main form and the gratitude formset are valid, preventing orphaned entries.
    """

    def get(self, request):
        """Render a blank entry form with empty gratitude formset."""
        form = EntryForm()
        formset = GratitudeFormSet()
        return render(
            request, "journal/entry_form.html", {"form": form, "formset": formset}
        )

    def post(self, request):
        """Process form submission to create a new entry.

        Validates the main entry form, then uses a database transaction to
        save the entry and validate/save gratitude items. If the gratitude
        formset is invalid, the transaction is rolled back to prevent saving
        an entry without valid gratitude items.
        """
        form = EntryForm(request.POST)
        if form.is_valid():
            try:
                # Use atomic transaction to rollback if gratitude formset is invalid
                with transaction.atomic():
                    # Save entry with current user
                    entry = form.save(commit=False)
                    entry.user = request.user
                    entry.save()
                    # Bind formset to saved entry and validate
                    formset = GratitudeFormSet(request.POST, instance=entry)
                    if not formset.is_valid():
                        # Trigger rollback by raising exception
                        raise ValueError("gratitude formset invalid")
                    formset.save()
                messages.success(
                    request, f'Entry "{entry.title}" created successfully!'
                )
                return redirect("journal:entry_create_success")
            except ValueError:
                # Formset contains validation errors will be rendered below
                messages.error(request, "Please correct the errors in the form.")
        else:
            # Main form invalid bind formset to preserve user input
            formset = GratitudeFormSet(request.POST)
            messages.error(request, "Please correct the errors in the form.")
        return render(
            request, "journal/entry_form.html", {"form": form, "formset": formset}
        )


class EntryListView(LoginRequiredMixin, ListView):
    """Display a paginated list of the current user's journal entries.

    Supports search across entry title, content, mood, and gratitude items.
    Results are ordered by date (newest first) and paginated at 10 per page.
    """

    model = Entry
    template_name = "journal/entry_list.html"
    context_object_name = "entries"
    paginate_by = 10

    def get_queryset(self):
        """Filter entries for current user and apply optional search.

        Uses prefetch_related for gratitude_items to minimize database queries.
        Search term is matched against title, content, mood, and gratitude text.
        """
        queryset = Entry.objects.filter(user=self.request.user).prefetch_related(
            "gratitude_items"
        )
        # Apply search filter if a search term is provided, matching across multiple fields.
        search = self.request.GET.get("search", "").strip()
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(content__icontains=search)
                | Q(mood__icontains=search)
                | Q(gratitude_items__item_text__icontains=search)
            ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        """Add the search term to context for template rendering."""
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get("search", "")
        return context


class EntryDetailView(LoginRequiredMixin, DetailView):
    """Display a single journal entry with its gratitude items.

    Only shows entries belonging to the current user. Uses prefetch_related
    to efficiently load associated gratitude items in a single query.
    """

    model = Entry
    template_name = "journal/entry_detail.html"
    context_object_name = "entry"

    def get_queryset(self):
        """Restrict to current user's entries and prefetch gratitude items."""
        return Entry.objects.filter(user=self.request.user).prefetch_related(
            "gratitude_items"
        )


class EntryDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a journal entry with user confirmation.

    Only allows deletion of entries belonging to the current user.
    Shows success/error messages and redirects to entry list on completion.
    """

    model = Entry
    template_name = "journal/entry_confirm_delete.html"
    success_url = reverse_lazy("journal:entry_list")

    def get_queryset(self):
        """Restrict deletion to current user's entries only."""
        return Entry.objects.filter(user=self.request.user)

    def form_valid(self, form):
        """Delete the entry and show appropriate success or error message."""
        entry_title = self.get_object().title
        try:
            response = super().form_valid(form)
            messages.success(self.request, f'"{entry_title}" was deleted successfully.')
            return response
        except Exception:
            messages.error(
                self.request, f'Could not delete "{entry_title}". Please try again.'
            )
            return redirect(self.success_url)


class EntryUpdateView(LoginRequiredMixin, View):
    """View for editing an existing journal entry and its gratitude items.

    GET: Display populated form with existing entry data and gratitude items.
    POST: Validate and save changes to entry and associated gratitude items.

    Only allows editing entries belonging to the current user.
    """

    def get_object(self, pk):
        """Retrieve entry by pk, ensuring it belongs to current user.

        Raises Http404 if entry doesn't exist or belongs to another user.
        """
        return get_object_or_404(Entry, pk=pk, user=self.request.user)

    def get(self, request, pk):
        """Render form populated with existing entry and gratitude items."""
        entry = self.get_object(pk)
        form = EntryForm(instance=entry)
        existing_count = entry.gratitude_items.count()
        extra = max(0, 3 - existing_count)
        EditFormSet = make_gratitude_edit_formset(extra=extra)
        formset = EditFormSet(instance=entry)
        return render(
            request,
            "journal/entry_form.html",
            {"form": form, "formset": formset, "is_edit": True, "entry": entry},
        )

    def post(self, request, pk):
        """Process form submission to update the entry.

        Validates both the entry form and gratitude formset. Only saves if
        both are valid. Since the entry already exists in the database,
        no transaction is needed (formset is bound to existing instance).
        """
        entry = self.get_object(pk)
        form = EntryForm(request.POST, instance=entry)
        formset = GratitudeEditFormSet(request.POST, instance=entry)
        if form.is_valid() and formset.is_valid():
            entry = form.save()
            formset.save()
            messages.success(request, f'Entry "{entry.title}" updated successfully!')
            return redirect("journal:entry_detail", pk=entry.pk)
        else:
            messages.error(request, "Please correct the errors in the form.")
        return render(
            request,
            "journal/entry_form.html",
            {"form": form, "formset": formset, "is_edit": True, "entry": entry},
        )


class HomeView(TemplateView):
    """Display the application home page with a random inspirational quote.

    Accessible to all users (authenticated and anonymous). Shows a randomly
    selected quote from the database, or None if no quotes exist.
    """

    template_name = "journal/home.html"

    def get_context_data(self, **kwargs):
        """Add a random quote to the template context.

        Uses order_by('?') for random selection. Gracefully handles cases
        where no quotes exist in the database.
        """
        context = super().get_context_data(**kwargs)
        try:
            # Select a random quote from the database
            context["quote"] = Quote.objects.order_by("?").first()
        except Exception:
            # No quotes available or database error
            context["quote"] = None
        return context

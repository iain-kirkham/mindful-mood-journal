from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView

from .forms import EntryForm, GratitudeEditFormSet, GratitudeFormSet
from .models import Entry


class EntryCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = EntryForm()
        formset = GratitudeFormSet()
        return render(request, "journal/entry_form.html", {"form": form, "formset": formset})

    def post(self, request):
        form = EntryForm(request.POST)
        formset = GratitudeFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            formset.instance = entry
            formset.save()
            return redirect("journal:entry_create_success")
        return render(request, "journal/entry_form.html", {"form": form, "formset": formset})


class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = "journal/entry_list.html"
    context_object_name = "entries"
    paginate_by = 10

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user).prefetch_related("gratitude_items")


class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry
    template_name = "journal/entry_detail.html"
    context_object_name = "entry"

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user).prefetch_related("gratitude_items")


class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model = Entry
    template_name = "journal/entry_confirm_delete.html"
    success_url = reverse_lazy("journal:entry_list")

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)


class EntryUpdateView(LoginRequiredMixin, View):
    def get_object(self, pk):
        return get_object_or_404(Entry, pk=pk, user=self.request.user)

    def get(self, request, pk):
        entry = self.get_object(pk)
        form = EntryForm(instance=entry)
        formset = GratitudeEditFormSet(instance=entry)
        return render(
            request,
            "journal/entry_form.html",
            {"form": form, "formset": formset, "is_edit": True, "entry": entry},
        )

    def post(self, request, pk):
        entry = self.get_object(pk)
        form = EntryForm(request.POST, instance=entry)
        formset = GratitudeEditFormSet(request.POST, instance=entry)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("journal:entry_detail", pk=entry.pk)
        return render(
            request,
            "journal/entry_form.html",
            {"form": form, "formset": formset, "is_edit": True, "entry": entry},
        )

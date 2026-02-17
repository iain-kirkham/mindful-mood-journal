from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .forms import EntryForm, GratitudeFormSet
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

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import EntryForm, GratitudeFormSet


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

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, DetailView, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib import messages

from .forms import EntryForm, GratitudeEditFormSet, GratitudeFormSet
from .models import Entry, Quote


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
        queryset = Entry.objects.filter(user=self.request.user).prefetch_related("gratitude_items")
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
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get("search", "")
        return context


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

    def form_valid(self, form):
        entry_title = self.get_object().title
        try:
            response = super().form_valid(form)
            messages.success(self.request, f'"{entry_title}" was deleted successfully.')
            return response
        except Exception:
            messages.error(self.request, f'Could not delete "{entry_title}". Please try again.')
            return redirect(self.success_url)


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


class HomeView(TemplateView):
    template_name = "journal/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["quote"] = Quote.objects.order_by("?").first()
        except Exception:
            context["quote"] = None
        return context

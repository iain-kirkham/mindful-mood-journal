from django.urls import path
from .views import EntryCreateView, EntryDetailView, EntryListView
from django.views.generic import TemplateView

app_name = "journal"

urlpatterns = [
    path("entries/", EntryListView.as_view(), name="entry_list"),
    path("entries/<int:pk>/", EntryDetailView.as_view(), name="entry_detail"),
    path("entries/create/", EntryCreateView.as_view(), name="entry_create"),
    path("entries/create/success/", TemplateView.as_view(template_name="journal/create_success.html"), name="entry_create_success"),
]

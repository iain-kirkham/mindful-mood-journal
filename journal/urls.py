from django.urls import path
from .views import EntryCreateView
from django.views.generic import TemplateView

app_name = "journal"

urlpatterns = [
    path("entries/create/", EntryCreateView.as_view(), name="entry_create"),
    path("entries/create/success/", TemplateView.as_view(template_name="journal/create_success.html"), name="entry_create_success"),
]

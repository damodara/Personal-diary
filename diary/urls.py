from django.urls import path

from . import views
from .apps import DiaryConfig

app_name = DiaryConfig.name

urlpatterns = [
    path("", views.my_entries_list, name="entry_list"),
    path("entry/<int:pk>/", views.entry_detail, name="entry_detail"),
    path("entry/create/", views.entry_create, name="entry_create"),
    path("entry/<int:pk>/edit/", views.entry_edit, name="entry_edit"),
    path("entry/<int:pk>/delete/", views.entry_delete, name="entry_delete"),
]

"""URL routes for master profiles and schedule management."""

from django.urls import path

from .views import (
    master_admin_list,
    master_create,
    master_delete,
    master_list,
    master_schedule,
    master_update,
    slot_admin_list,
    slot_create,
    slot_delete,
    slot_update,
)

app_name = "masters"


urlpatterns = [
    path("", master_list, name="list"),
    path("schedule/", master_schedule, name="schedule"),
    path("admin/", master_admin_list, name="admin_list"),
    path("admin/create/", master_create, name="create"),
    path("admin/<int:pk>/edit/", master_update, name="update"),
    path("admin/<int:pk>/delete/", master_delete, name="delete"),
    path("slots/", slot_admin_list, name="slot_list"),
    path("slots/create/", slot_create, name="slot_create"),
    path("slots/<int:pk>/edit/", slot_update, name="slot_update"),
    path("slots/<int:pk>/delete/", slot_delete, name="slot_delete"),
]
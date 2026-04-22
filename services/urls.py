"""URL routes for salon service pages."""

from django.urls import path

from .views import (
    service_admin_list,
    service_create,
    service_delete,
    service_list,
    service_update,
)

app_name = "services"


urlpatterns = [
    path("", service_list, name="list"),
    path("admin/", service_admin_list, name="admin_list"),
    path("admin/create/", service_create, name="create"),
    path("admin/<int:pk>/edit/", service_update, name="update"),
    path("admin/<int:pk>/delete/", service_delete, name="delete"),
]
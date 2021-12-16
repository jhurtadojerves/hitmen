"""Auth models."""

# Django
from django.urls import path

# Local
from apps.hits.views import (
    HitListView,
    HitDetailView,
    HitCreateView,
    HitUpdateView,
    HitBulkUpdate,
)

app_name = "hits"

urlpatterns = (
    path(
        route="hits/",
        view=HitListView.as_view(),
        name="list",
    ),
    path(
        route="hits/bulk/",
        view=HitBulkUpdate.as_view(),
        name="bulk",
    ),
    path(
        route="hits/create/",
        view=HitCreateView.as_view(),
        name="create",
    ),
    path(
        route="hits/<int:pk>/",
        view=HitDetailView.as_view(),
        name="detail",
    ),
    path(
        route="hits/<int:pk>/edit/",
        view=HitUpdateView.as_view(),
        name="update",
    ),
)

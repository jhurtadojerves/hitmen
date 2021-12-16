"""Auth models."""

# Django
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

# Views
from apps.authentication.views import (
    HitmanListView,
    HitmanDetailView,
    CreateBossView,
    RegisterView,
)

app_name = "auth"

urlpatterns = (
    # path(
    #    route="register/",
    #    view=RegisterView.as_view(),
    #    name="register",
    # ),
    path(
        route="",
        view=LoginView.as_view(
            template_name="authentication/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path(
        route="register/",
        view=RegisterView.as_view(),
        name="register",
    ),
    path(
        route="logout/",
        view=LogoutView.as_view(),
        name="logout",
    ),
    path(
        route="hitmen/",
        view=login_required(HitmanListView.as_view()),
        name="hitmen_list",
    ),
    path(
        route="hitmen/<int:pk>/",
        view=login_required(HitmanDetailView.as_view()),
        name="hitmen_detail",
    ),
    path(
        route="hitmen/manager/",
        view=login_required(CreateBossView.as_view()),
        name="hitmen_assign_manager",
    ),
)

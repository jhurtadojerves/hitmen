# Django
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.views.generic import UpdateView, DetailView, CreateView, ListView


# Forms
from apps.authentication.forms import RegisterForm, CreateBossForm

User = get_user_model()


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "authentication/register.html"
    success_url = reverse_lazy("auth:login")

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS, "Successfully hitman registered"
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "An error has occurred")
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)


class HitmanListView(PermissionRequiredMixin, ListView):
    model = User

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.id == 1:
            queryset = queryset.filter(Q(id=user.id) | Q(boss=user))
        return queryset

    def has_permission(self):
        user = self.request.user
        return user.id == 1 or user.is_staff


class HitmanDetailView(PermissionRequiredMixin, DetailView):
    model = User

    def has_permission(self):
        user = self.request.user
        self.object = self.get_object()

        if user.pk == 1:
            return True
        if self.object.pk == user.pk:
            return True
        if self.object.boss.pk == user.pk:
            return True
        return False


class CreateBossView(PermissionRequiredMixin, UpdateView):
    form_class = CreateBossForm

    def form_valid(self, form):
        hitmen = form.cleaned_data.get("hitmen")
        if hitmen:
            hitmen.update(is_staff=True, boss=False)
        messages.add_message(self.request, messages.SUCCESS, "Successfully create boss")
        return redirect(reverse_lazy("auth:hitmen_list"))

    def form_invalid(self, form):
        messages.add_message(
            self.request,
            messages.ERROR,
            "An error has occurred, please verify input data",
        )
        return redirect(reverse_lazy("hitmen_list"))

    def has_permission(self):
        return self.request.user.id == 1

# Django
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import reverse, redirect
from django.core.exceptions import ValidationError

# Local
from apps.hits.models import Hit
from apps.authentication.models import User
from apps.hits.forms import (
    CreateHitForm,
    UpdateHitFormActiveHitman,
    UpdateHitFormInactiveHitman,
    BulkUpdateHitForm,
)


class BaseFormHit:
    model = Hit
    success_message = "created"

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "An error has occurred")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f"The hit was {self.success_message} correctly ",
        )
        return super().form_valid(form)


class HitListView(LoginRequiredMixin, ListView):
    model = Hit

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if not user.pk == 1:
            subordinates = user.subordinates.all()
            if len(subordinates):
                return queryset.filter(Q(assigned=user) | Q(assigned__in=subordinates))
            return queryset.filter(assigned=user)
        return queryset


class HitBulkUpdate(LoginRequiredMixin, FormView):
    model = Hit
    template_name = "hits/hit_bulk.html"
    form_class = BulkUpdateHitForm

    def post(self, request, *args, **kwargs):
        hits_id = request.POST.getlist("hits", ())
        hitman_id = request.POST.get("hitman", False)
        if not hits_id:
            form = self.get_form()
            messages.add_message(
                self.request, messages.ERROR, "Please select hits to continue"
            )
            return self.form_invalid(form)
        if not hitman_id:
            form = self.get_form()
            messages.add_message(
                self.request, messages.ERROR, "Please select a hitman to continue"
            )
            return self.form_invalid(form)
        hits = Hit.objects.filter(pk__in=hits_id)
        hitman = User.objects.get(pk=hitman_id)
        hits.update(assigned=hitman)
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f"The hits was reassignment correctly ",
        )
        return redirect(reverse("hits:bulk"))


class HitDetailView(LoginRequiredMixin, DetailView):
    model = Hit


class HitCreateView(LoginRequiredMixin, BaseFormHit, CreateView):
    form_class = CreateHitForm


class HitUpdateView(PermissionRequiredMixin, BaseFormHit, UpdateView):
    success_message = "updated"
    template_name = "hits/hit_update.html"

    def has_permission(self):
        self.object = self.get_object()
        if self.object.state != 1:
            return False
        return True

    def get_form_class(self):
        self.object = self.get_object()
        if self.object.assigned.state == 1:
            return UpdateHitFormActiveHitman
        else:
            return UpdateHitFormInactiveHitman

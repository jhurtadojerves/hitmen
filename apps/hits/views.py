# Django
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import Q
from django.contrib import messages

# Local
from apps.hits.models import Hit
from apps.hits.forms import CreateHitForm


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


class HitDetailView(DetailView):
    model = Hit


class HitCreateView(CreateView):
    model = Hit
    form_class = CreateHitForm

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "An error has occurred")
        return super(HitCreateView, self).form_invalid(form)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS, "The hit was created correctly "
        )
        return super(HitCreateView, self).form_valid(form)

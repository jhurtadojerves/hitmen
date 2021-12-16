"""Hit app forms"""
# Django
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db.models import Q

# Third party integration
from tracing.middleware import TracingMiddleware

# Local
from apps.hits.models import Hit

User = get_user_model()


class BaseHitForm(forms.ModelForm):
    def get_base_queryset(self):
        information = TracingMiddleware.get_info()
        user = information.get("user", False)
        if user.pk == 1:
            queryset = User.objects.filter(state=1)
        else:
            queryset = user.subordinates.filter(state=1)
        if self.instance and self.instance.id:
            queryset = User.objects.filter(Q(state=1) | Q(pk=self.instance.assigned.pk))
        return queryset


class CreateHitForm(BaseHitForm):
    class Meta:
        model = Hit
        fields = ("target_name", "mission_description", "assigned")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = self.get_base_queryset()
        if self.instance and self.instance.id:
            queryset = User.objects.filter(Q(state=1) | Q(pk=self.instance.assigned.pk))
        self.fields["assigned"].queryset = queryset

    def clean_assigned(self):
        """Method to validate assigned field"""
        assigned = self.cleaned_data.get("assigned", False)
        if not assigned:
            raise ValidationError("This field is required.")
        return assigned


class UpdateHitFormActiveHitman(BaseHitForm):
    DISABLED = True

    class Meta:
        model = Hit
        fields = ("target_name", "mission_description", "assigned")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = self.get_base_queryset()
        self.fields["assigned"].queryset = queryset
        self.fields["target_name"].disabled = self.DISABLED
        self.fields["mission_description"].disabled = self.DISABLED
        self.fields["assigned"].disabled = not self.DISABLED


class UpdateHitFormInactiveHitman(UpdateHitFormActiveHitman):
    DISABLED = False

    class Meta:
        model = Hit
        fields = ("target_name", "mission_description", "assigned")


class BulkUpdateHitForm(forms.Form):
    hits = forms.ModelMultipleChoiceField(
        queryset=Hit.objects.filter(state=1), widget=forms.CheckboxSelectMultiple()
    )
    hitman = forms.ModelChoiceField(
        queryset=User.objects.filter(state=1), label="New hitman"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset_hitmen, queryset_hits = self.get_base_queryset()
        self.fields["hits"].queryset = queryset_hits
        self.fields["hitman"].queryset = queryset_hitmen

    def get_base_queryset(self):
        information = TracingMiddleware.get_info()
        user = information.get("user", False)
        if user.pk == 1:
            queryset_hitmen = User.objects.filter(state=1)
        else:
            queryset_hitmen = user.subordinates.filter(state=1) | User.objects.filter(
                pk=user.pk
            )
        queryset_hits = Hit.objects.filter(state=1, assigned__in=queryset_hitmen)

        return queryset_hitmen, queryset_hits

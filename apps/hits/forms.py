"""Hit app forms"""
# Django
from django import forms
from django.core.exceptions import ValidationError

# Local
from apps.hits.models import Hit


class CreateHitForm(forms.ModelForm):
    class Meta:
        model = Hit
        fields = ("target_name", "mission_description", "assigned")

    def clean_assigned(self):
        """Method to validate assigned field"""
        assigned = self.cleaned_data.get("assigned", False)
        if not assigned:
            raise ValidationError("This field is required.")

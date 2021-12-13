"""Forms to auth app"""

# Django
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

#

User = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")


class CreateBossForm(forms.Form):
    hitmen = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(
            boss__isnull=True, state=User.STATE.ACTIVE
        ).exclude(id=1),
        label="Available hitmen",
    )

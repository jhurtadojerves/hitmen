"""Forms to auth app"""

# Django
from django.contrib.auth.forms import UserCreationForm
from apps.authentication.models import User
from django import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True


class CreateBossForm(forms.Form):
    hitmen = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(
            boss__isnull=True, state=User.STATE.ACTIVE
        ).exclude(id=1),
        label="Available hitmen",
    )

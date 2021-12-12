"""User model."""

# Django
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Third party integration
from django_fsm import FSMIntegerField, transition


class User(AbstractUser):
    """User model.

    Extend from Django's Abstract User, change the username field
    to email and add some extra fields.
    """

    class STATE(models.IntegerChoices):
        INACTIVE = 0
        ACTIVE = 1

    email = models.EmailField(
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    boss = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        related_name="subordinates",
    )
    state = FSMIntegerField(choices=STATE.choices, default=STATE.ACTIVE, protected=True)
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    def __str__(self):
        """Return username."""
        return self.username

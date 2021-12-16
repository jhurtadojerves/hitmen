"""User model."""

# Django
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse

# Third party integration
from django_fsm import FSMIntegerField, transition

# Conditions
from apps.authentication.conditions import (
    verify_if_user_is_the_boss,
    verify_if_hitman_is_not_the_boss,
)


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
    description = models.TextField(default="")
    state = FSMIntegerField(choices=STATE.choices, default=STATE.ACTIVE, protected=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        ordering = ("pk",)

    def __str__(self):
        """Return username."""
        return f"{self.get_full_name()} ({self.get_state_display()})"

    def get_detail_url(self):
        return reverse(
            "auth:hitmen_detail",
            args=[
                self.pk,
            ],
        )

    def get_list_url(self):
        return reverse("auth:hitmen_list")

    @transition(
        field="state",
        source=STATE.ACTIVE,
        target=STATE.INACTIVE,
        conditions=[verify_if_user_is_the_boss, verify_if_hitman_is_not_the_boss],
        custom=dict(
            verbose="Disable user",
            btn="danger",
        ),
    )
    def disable(self, **kwargs):
        self.is_active = False
        pass

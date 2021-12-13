"""Models hits app"""

# Django
from django.db import models
from django.shortcuts import reverse

# Third party integration
from django_fsm import FSMIntegerField, transition
from django.core.exceptions import ValidationError


class Hit(models.Model):
    """
    Model for assigning murders
    """

    class STATE(models.IntegerChoices):
        FAILED = 0
        ASSIGNED = 1
        COMPLETED = 2

    target_name = models.CharField(max_length=256)
    mission_description = models.TextField()
    assigned = models.ForeignKey(
        to="authentication.User", on_delete=models.PROTECT, related_name="hits_assigned"
    )
    creator = models.ForeignKey(
        "authentication.User",
        null=True,
        on_delete=models.PROTECT,
        related_name="hits_creator",
    )
    state = FSMIntegerField(
        choices=STATE.choices, default=STATE.ASSIGNED, protected=True
    )

    def get_detail_url(self):
        breakpoint()
        return reverse(
            "hits:detail",
            args=[
                self.pk,
            ],
        )

    def get_list_url(self):
        breakpoint()
        return reverse("hits:list")

    def clean(self):
        if not hasattr(self, "assigned"):
            raise ValidationError("Assigned field is required.")
        if not self.pk:
            if self.assigned and self.assigned.STATE == 0:
                raise ValidationError(
                    "The selected hitman is inactive, please select a valid Hitman"
                )
        else:
            hit = Hit.objects.get(pk=self.pk)
            if hit.assigned.pk != self.assigned.pk and self.assigned.STATE == 0:
                raise ValidationError(
                    "The selected hitman is inactive, please select a valid Hitman"
                )

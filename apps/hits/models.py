"""Models hits app"""

# Django
from django.db import models

# Third party integration
from django_fsm import FSMIntegerField, transition


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

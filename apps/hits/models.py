"""Models hits app"""

# Django
from django.db import models
from django.shortcuts import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

# Third party integration
from django_fsm import FSMIntegerField, transition
from django.core.exceptions import ValidationError

# Local
from apps.hits.conditions import check_permissions


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

    def __str__(self):
        return f"Hit #{self.pk}"

    def get_detail_url(self):
        return reverse(
            "hits:detail",
            args=[
                self.pk,
            ],
        )

    def get_absolute_url(self):
        return self.get_detail_url()

    def get_list_url(self):
        return reverse("hits:list")

    """
        def clean(self):
        if hasattr(self, "assigned"):
            if not self.pk:
                if self.assigned.STATE == 0:
                    raise ValidationError(
                        "The selected hitman is inactive, please select a valid Hitman"
                    )
            else:
                hit = Hit.objects.get(pk=self.pk)
                if hit.assigned.pk != self.assigned.pk and self.assigned.STATE == 0:
                    raise ValidationError(
                        "The selected hitman is inactive, please select a valid Hitman"
                    )

    """

    @transition(
        field="state",
        source=STATE.ASSIGNED,
        target=STATE.FAILED,
        conditions=[
            check_permissions,
        ],
        custom=dict(
            verbose="Mark as Failed",
            btn="danger",
        ),
    )
    def failed(self, **kwargs):
        pass

    @transition(
        field="state",
        source=STATE.ASSIGNED,
        target=STATE.COMPLETED,
        conditions=[
            check_permissions,
        ],
        custom=dict(
            verbose="Mark as Completed",
            btn="success",
        ),
    )
    def completed(self, **kwargs):
        pass


@receiver(post_save, sender=Hit)
def add_creator(sender, instance, created, **kwargs):
    if created:
        from tracing.middleware import TracingMiddleware

        information = TracingMiddleware.get_info()
        user = information.get("user", False)
        instance.creator = user
        instance.save()

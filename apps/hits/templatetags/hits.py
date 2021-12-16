from django import template
from apps.hits.models import Hit

register = template.Library()


@register.simple_tag()
def get_hit_by_pk(pk):
    breakpoint()
    return pk.data["value"].instance

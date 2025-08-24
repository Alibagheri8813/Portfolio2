from django import template
from django.utils.html import format_html
import math

register = template.Library()

@register.filter
def reading_time(text: str) -> str:
    words = len((text or "").split())
    minutes = max(1, math.ceil(words / 200))
    return f"{minutes} min read"

@register.simple_tag
def sr_only(text: str):
    return format_html('<span class="sr-only">{}</span>', text)
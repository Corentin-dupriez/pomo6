from django import template

from chat.models import Thread

register = template.Library()

@register.filter
def other_participant(thread: Thread, current_user) -> int:
    participants = Thread.objects.filter(pk=thread.pk).values_list('participants', flat=True)
    return [p for p in participants if p != current_user][0]

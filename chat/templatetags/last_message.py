from django import template

from chat.models import Message

register = template.Library()

@register.filter
def last_message(thread) -> Message:
    return Message.objects.filter(thread_id=thread.pk).order_by('-pk').first()

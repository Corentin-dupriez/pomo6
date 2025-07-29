from django import template

from chat.models import Message, Thread

register = template.Library()

@register.filter
def last_message(thread: Thread) -> Message:
    """
    Takes a thread object and returns the most recent message in the thread.
    :param thread: a thread object
    :return: the most recent message in the thread
    """
    return Message.objects.filter(thread_id=thread.pk).order_by('-pk').first()

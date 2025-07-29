from django import template

from chat.models import Thread

register = template.Library()

@register.filter
def other_participant(thread: Thread, current_user: int) -> int:
    """
    Takes the thread object and the current user ID and returns the id of the other chat participant
    :param thread: the Thread object
    :param current_user: the primary key of the current user
    :return: int: the id of the other chat participant
    """
    participants = Thread.objects.filter(pk=thread.pk).values_list('participants', flat=True)
    return [p for p in participants if p != current_user][0]

from django import template
from notifications.models import Notification

register = template.Library()

@register.simple_tag(takes_context=True)
def notification_tag(context, **kwargs):
    request = context['request']
    if request.user.is_authenticated:
        return Notification.objects.filter(target_user=request.user, read=False).count()
    return 0
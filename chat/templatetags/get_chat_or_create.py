from django import template

from chat.models import Thread

register = template.Library()

@register.simple_tag(name='get_chat_or_create')
def get_chat_or_create(user, advert :"adverts.Advertisement"):
    chat = Thread.objects.filter(advert=advert, participants=user).first()

    if chat:
        return chat.pk

    chat = Thread.objects.create(advert_id=advert.pk)
    chat.participants.add(user, advert.user)
    chat.save()

    return chat.pk

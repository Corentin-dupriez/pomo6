from django.dispatch import receiver
from adverts.models import Advertisement
from search_indexing.utils import index_ad
from django.db.models import signals


@receiver(signals.post_save, sender=Advertisement)
def index_advertisement(sender, instance: Advertisement, created, **kwargs):
    if created:
        index_ad(instance)

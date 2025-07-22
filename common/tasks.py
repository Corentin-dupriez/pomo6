from celery import shared_task
from django.apps import apps

from common.utils import convert_to_webp


@shared_task
def convert_image_task(app_label, model_name, instance_id, image_field='image'):
    model = apps.get_model(app_label, model_name)
    instance = model.objects.get(pk=instance_id)
    image_field = getattr(instance, image_field)
    if image_field is not None:
        file_name, content = convert_to_webp(image_field)
        image_field.save(file_name, content, save=True)
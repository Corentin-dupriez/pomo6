from celery import shared_task
from django.apps import apps
import os
from django.core.mail import send_mail
from django.template.loader import render_to_string
from common.utils import convert_to_webp


@shared_task
def convert_image_task(app_label, model_name, instance_id, image_field='image'):
    model = apps.get_model(app_label, model_name)
    instance = model.objects.get(pk=instance_id)
    image_field = getattr(instance, image_field)
    if image_field is not None:
        file_name, content = convert_to_webp(image_field)
        image_field.save(file_name, content, save=True)

@shared_task
def send_email(subject: str, from_email: str, to_email: str, action: str, context: dict):
    template_name = f'{action}.html'
    root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(root_folder, 'templates', 'emails', template_name)
    try:
        html_content = render_to_string(file_path, context)
    except:
        raise Exception('Failed to find template')

    send_mail(subject, html_content, from_email, [to_email], fail_silently=False)
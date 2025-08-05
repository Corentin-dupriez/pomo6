from celery import shared_task
from django.apps import apps
import os
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from common.utils import convert_to_webp


@shared_task
def convert_image_task(app_label, model_name, instance_id, image_field='image'):
    model = apps.get_model(app_label, model_name)
    instance = model.objects.get(pk=instance_id)
    image_field = getattr(instance, image_field)
    if image_field is not None and hasattr(image_field, 'name'):
        original_file_name = image_field.name.lower()
        if not original_file_name.endswith('.webp'):
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

    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send()
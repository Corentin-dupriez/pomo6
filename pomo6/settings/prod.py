from .base import *
from decouple import config
import ssl

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')

CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS').split(',')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [{
                "address": (config('REDIS_HOST'), config('REDIS_PORT', cast=int)),
                "password": config('REDIS_PASSWORD'),
                "ssl": True,
            }],
        },
    },
}

CELERY_BROKER_URL = f"rediss://:{config('REDIS_PASSWORD')}@{config('REDIS_HOST')}:{config('REDIS_PORT')}/0"

CELERY_BROKER_USE_SSL = {
    "ssl_cert_reqs": ssl.CERT_NONE,
}

CELERY_REDIS_BACKEND_USE_SSL = {
    "ssl_cert_reqs": ssl.CERT_NONE,
}

CELERY_RESULT_BACKEND=CELERY_BROKER_URL
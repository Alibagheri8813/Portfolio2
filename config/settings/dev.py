from .base import *  # noqa

DEBUG = True
ALLOWED_HOSTS = ALLOWED_HOSTS or ["*"]
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
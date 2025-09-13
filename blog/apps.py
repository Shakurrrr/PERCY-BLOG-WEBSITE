# blog/apps.py
from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"

    def ready(self):
        from . import signals  # register handlers; DO NOT query DB here

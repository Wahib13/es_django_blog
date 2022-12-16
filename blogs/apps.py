import os

from django.apps import AppConfig

from config.settings.base import APPS_DIR


class BlogsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # name = f'{os.path.basename(os.path.normpath(APPS_DIR))}.blogs'
    name = 'blogs'

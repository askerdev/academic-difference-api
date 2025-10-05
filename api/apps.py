"""Django api application configuration"""

from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Configuration for api app"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

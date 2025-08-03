"""
Cart app config.
"""

from django.apps import AppConfig


class CartConfig(AppConfig):
    """
    Cart app config.

    Attributes:
        default_auto_field: Default auto-created primary key field.
        name: App name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'

"""
Urls for cart app.

Attributes:
    urlpatterns: All url paths available in the app with view specified.
"""

from django.urls import path
from .views import SendOrderView

urlpatterns: list[path] = [
    path('', SendOrderView.as_view(), name='send-order'),
]
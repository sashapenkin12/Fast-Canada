"""
Urls for cart app.

Attributes:
    urlpatterns: All url paths available in the app with view specified.
"""

from django.urls import path
from .views import (CartView, AddItemView, DeleteItemView,
                    DecreaseItemCountView, IncreaseItemCountView)

urlpatterns: list[path] = [
    path('', CartView.as_view(), name='cart'),
    path('add/', AddItemView.as_view(), name='add-cart-item'),
    path('remove/<int:item_id>/', DeleteItemView.as_view(), name='remove-cart-item'),
    path(
        'decrease/<int:item_id>/',
        DecreaseItemCountView.as_view(),
        name='decrease-item-count',
    ),
    path(
        'increase/<int:item_id>/',
        IncreaseItemCountView.as_view(),
        name='decrease-item-count',
    ),
]

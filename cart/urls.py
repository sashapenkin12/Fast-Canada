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
    path('cart/add/', AddItemView.as_view(), name='add-cart-item'),
    path('cart/remove/<int:item_id>/', DeleteItemView.as_view(), name='remove-cart-item'),
    path(
        'cart/decrease/<int:item_id>/',
        DecreaseItemCountView.as_view(),
        name='decrease-item-count',
    ),
    path(
        'cart/increase/<int:item_id>/',
        IncreaseItemCountView.as_view(),
        name='decrease-item-count',
    ),
]

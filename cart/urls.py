"""
Urls for cart app.

Attributes:
    urlpatterns: All url paths available in the app with view specified.
"""

from django.urls import path

from .views import CartViewSet


urlpatterns: list[path] = [
    path('', CartViewSet.as_view({'get': 'list'}), name='cart-list'),
    path('add/', CartViewSet.as_view({'post': 'create'}), name='add-cart-item'),
    path('remove/<int:pk>/', CartViewSet.as_view({'delete': 'destroy'}), name='remove-cart-item'),
    path('increase/<int:pk>/', CartViewSet.as_view({'patch': 'increase'}), name='cart-item-increase'),
    path('decrease/<int:pk>/', CartViewSet.as_view({'patch': 'decrease'}), name='cart-item-decrease'),
]

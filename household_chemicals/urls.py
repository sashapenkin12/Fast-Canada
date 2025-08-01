from django.urls import path
from household_chemicals.views import CatalogView, ProductDetailView

urlpatterns = [
    path('/', CatalogView.as_view(), name='product-list'),
    path('/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]

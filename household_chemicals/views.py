from rest_framework.generics import ListAPIView, RetrieveAPIView

from household_chemicals.serializers import ProductBaseSerializer, ProductDetailSerializer
from household_chemicals.models import ChemicalProduct
from household_chemicals.paginations import ProductPagination


class CatalogView(ListAPIView):
    queryset = ChemicalProduct.objects.all().order_by('id')
    serializer_class = ProductBaseSerializer
    pagination_class = ProductPagination


class ProductDetailView(RetrieveAPIView):
    queryset = ChemicalProduct.objects.all()
    serializer_class = ProductDetailSerializer

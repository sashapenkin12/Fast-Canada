from rest_framework.generics import ListAPIView, RetrieveAPIView

from household_chemicals.serializers import ProductBaseSerializer, ProductDetailSerializer
from household_chemicals.models import ChemicalProduct
from household_chemicals.paginations import ProductPagination


class CatalogView(ListAPIView):
    serializer_class = ProductBaseSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        return ChemicalProduct.objects.only(
            'id', 'title', 'image', 'price', 'full_description', 'is_available'
        ).order_by('id')


class ProductDetailView(RetrieveAPIView):
    queryset = ChemicalProduct.objects.all()
    serializer_class = ProductDetailSerializer

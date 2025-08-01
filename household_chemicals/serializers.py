from rest_framework import serializers

from household_chemicals.models import ChemicalProduct


class ProductBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChemicalProduct
        fields = ('title', 'image', 'price', 'is_available')


class ProductDetailSerializer(ProductBaseSerializer):
    description = serializers.CharField(
        style={'base_template': 'textarea.html'},
        source='full_description',
    )

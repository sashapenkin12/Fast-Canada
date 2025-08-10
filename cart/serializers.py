"""
Serializers for cart app.
"""

from rest_framework import serializers

from decimal import Decimal

from household_chemicals.models import ChemicalProduct

class AddCartItemSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=ChemicalProduct.objects.all())
    count = serializers.IntegerField(min_value=1)


class CartProductSerializer(serializers.ModelSerializer):
    """
    Serializer for representing products in DB.
    """
    class Meta:
        model = ChemicalProduct
        fields = ('title', 'price', 'is_available')


class CartItemSerializer(serializers.Serializer):
    """
    Serializer for representing cart items.

    Attributes:
        id: Cart item ID.
        product: Cart item's product.
        count: Products count.
        total_price: Total price of specified amount of products.
    """
    id = serializers.IntegerField()
    product = CartProductSerializer()
    count = serializers.IntegerField(min_value=1)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj: dict) -> str:
        """
        Get total price of specified amount of products.

        Attributes:
            obj: Serializer object.

        Returns:
            Decimal: Total price.
        """
        return str(Decimal(obj['product']['price']) * obj['count'])

"""
Serializers for cart app.
"""

from rest_framework import serializers

from decimal import Decimal


class CartProductSerializer(serializers.Serializer):
    """
    Serializer for representing products in DB.

    Attributes:
        title: Title of the product.
        price: Product price.
    """
    title = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)


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

    def get_total_price(self, obj: dict) -> Decimal:
        """
        Get total price of specified amount of products.

        Attributes:
            obj: Serializer object.

        Returns:
            Decimal: Total price.
        """
        return obj['product']['price'] * obj['count']

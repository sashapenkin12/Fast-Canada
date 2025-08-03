from rest_framework import serializers


class CartProductSerializer(serializers.Serializer):
    title = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)


class CartItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product = CartProductSerializer()
    count = serializers.IntegerField()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return obj['product']['price'] * obj['count']

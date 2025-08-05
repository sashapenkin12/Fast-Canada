from rest_framework import serializers


class ProductBaseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    image = serializers.ImageField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    is_available = serializers.BooleanField()


class ProductDetailSerializer(ProductBaseSerializer):
    description = serializers.CharField(
        style={'base_template': 'textarea.html'},
        source='full_description',
    )

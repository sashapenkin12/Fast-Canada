from rest_framework import serializers

class ProductBaseSerializer(serializers.Serializer):
    image = serializers.ImageField(source='image')
    title = serializers.CharField(source='title')
    price = serializers.IntegerField(source='price')
    is_available = serializers.BooleanField(source='is_available')


class ProductDetailSerializer(ProductBaseSerializer):
    full_description = serializers.CharField(style={'base_template': 'textarea.html'})

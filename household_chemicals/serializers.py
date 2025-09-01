from rest_framework import serializers
from .models import ChemicalProduct

class ProductBaseSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ChemicalProduct
        fields = ['id', 'title', 'image_url', 'price', 'description', 'is_available']

    @staticmethod
    def get_description(obj):
        if obj.full_description:
            return obj.full_description[:100]
        return ""

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    description = serializers.CharField(
        style={'base_template': 'textarea.html'},
        source='full_description'
    )

    class Meta(ProductBaseSerializer.Meta):
        model = ChemicalProduct
        fields = '__all__'

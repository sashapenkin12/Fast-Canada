import phonenumbers
from rest_framework import serializers

from cart.serializers import CartItemSerializer


class OrderSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=255)
    phone_number = serializers.CharField()
    email = serializers.EmailField(required=False)
    items = CartItemSerializer(many=True, allow_empty=False)
    comment = serializers.CharField(style={'base_template': 'textarea.html'}, allow_blank=True, required=False)


    def validate_phone_number(self, value):
        try:
            parsed = phonenumbers.parse(value, None)
            if not phonenumbers.is_valid_number(parsed):
                raise serializers.ValidationError("Invalid phone number.")
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError("Wrong phone number format.")
        return value

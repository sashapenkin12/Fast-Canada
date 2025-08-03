import phonenumbers
from rest_framework import serializers

from cart.serializers import CartItemSerializer


class OrderSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=255)
    phone_number = serializers.CharField()
    email = serializers.EmailField()
    items = CartItemSerializer(many=True, allow_empty=False)


    def validate_phone_number(self, value):
        try:
            parsed = phonenumbers.parse(value, None)
            if not phonenumbers.is_valid_number(parsed):
                raise serializers.ValidationError("Некорректный номер телефона")
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError("Неверный формат номера")
        return value

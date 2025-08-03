from django.test import SimpleTestCase
from orders.serializers import OrderSerializer

VALID_PHONE = "+996700123456"

VALID_DATA = {
    "full_name": "Sasha",
    "address": "Bishkek, Chui",
    "phone_number": VALID_PHONE,
    "email": "sasha@example.com",
    "items": [
        {
            "id": 1,
            "product": {
                "title": "Product 1",
                "price": "100.00",
            },
            "count": 2
        }
    ]
}

class OrderSerializerTest(SimpleTestCase):

    def test_valid_data(self):
        serializer = OrderSerializer(data=VALID_DATA)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_phone_number(self):
        data = VALID_DATA.copy()
        data["phone_number"] = "12345"
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("phone_number", serializer.errors)
        self.assertIn(
            serializer.errors["phone_number"][0],
            ["Некорректный номер телефона", "Неверный формат номера"]
        )

    def test_missing_required_field(self):
        data = VALID_DATA.copy()
        data.pop("email")
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

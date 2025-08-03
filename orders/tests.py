from django.test import TestCase
from orders.serializers import OrderSerializer

VALID_DATA = {
    "first_name": "Асем",
    "last_name": "Таштанова",
    "email": "as@gmail.com",
    "phone": "+996500505050",
    "delivery_type": "pickup",
    "payment_type": "cash",
    "city": "Бишкек",
    "address": "Исанова 105",
    "items": [
        {
            "product": 1,
            "count": 2,
            "price": "150.00"
        }
    ]
}


class OrderSerializerTest(TestCase):

    def test_valid_data(self):
        serializer = OrderSerializer(data=VALID_DATA)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_phone(self):
        data = VALID_DATA.copy()
        data["phone"] = "0500505050"  # Без +996
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("phone", serializer.errors)

    def test_missing_email(self):
        data = VALID_DATA.copy()
        del data["email"]
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_invalid_email_format(self):
        data = VALID_DATA.copy()
        data["email"] = "notanemail"
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_empty_items_list(self):
        data = VALID_DATA.copy()
        data["items"] = []
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("items", serializer.errors)

    def test_negative_item_count(self):
        data = VALID_DATA.copy()
        data["items"][0]["count"] = -1
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("items", serializer.errors)

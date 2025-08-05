from django.test import SimpleTestCase

from orders.services.email_content import get_order_email_content
from orders.serializers import OrderSerializer


class OrderEmailContentTests(SimpleTestCase):
    def test_get_order_email_content(self):
        # Arrange: тестовые данные для заказа
        data = {
            'full_name': 'Тестовый Клиент',
            'phone_number': '+1234567890',
            'address': 'г. Бишкек, ул. Тестовая, 1',
            'products': ['Товар 1', 'Товар 2'],
        }

        # Act: получаем текст и HTML
        text_message, html_message = get_order_email_content(data)

        # Assert: проверяем, что ключевые данные есть в сообщениях
        self.assertIn('Тестовый Клиент', text_message)
        self.assertIn('Товар 1', text_message)
        self.assertIn('Товар 2', html_message)
        self.assertIn('Тестовый Клиент', html_message)


VALID_PHONE = "+996700123456"
VALID_ITEM = {
    "id": 1,
    "count": 2,
    "product": {
        "title": "Product 1",
        "price": "100.00",
    },
}
VALID_DATA = {
    "full_name": "Sasha",
    "address": "Bishkek, Chui",
    "phone_number": VALID_PHONE,
    "email": "sasha@example.com",
    "items": [
        VALID_ITEM,
    ],
}


class OrderSerializerTest(SimpleTestCase):

    def test_valid_data(self):
        serializer = OrderSerializer(data=VALID_DATA)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_phone(self):
        data = VALID_DATA.copy()
        data["phone_number"] = "0500505050"  # Без +996
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("phone_number", serializer.errors)

    def test_missing_email(self):
        data = VALID_DATA.copy()
        del data["email"]
        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid())

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
        item = VALID_ITEM.copy()
        item['count'] = -1
        data["items"] = [item]
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("items", serializer.errors)

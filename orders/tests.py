from django.test import TestCase
from orders.services.email_content import get_order_email_content

class OrderEmailContentTests(TestCase):
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
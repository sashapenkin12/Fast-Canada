from django.template.loader import render_to_string

def get_order_email_content(data):
    products = data.get('products', [])

    context = {
        'full_name': data.get('full_name', 'неизвестно'),
        'phone_number': data.get('phone_number', 'не указано'),
        'address': data.get('address', 'не указано'),
        'products': products,
    }

    html_message = render_to_string('orders/email/order_email.html', context)

    if products:
        products_str = "\n".join(f"- {item}" for item in products)
    else:
        products_str = "Нет товаров"

    text_message = (
        f"Поступил новый заказ от {context['full_name']}.\n"
        f"Телефон: {context['phone_number']}\n"
        f"Адрес: {context['address']}\n"
        f"Продукты:\n{products_str}"
    )

    return text_message, html_message

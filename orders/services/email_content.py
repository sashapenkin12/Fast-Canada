from django.template.loader import render_to_string

def get_order_email_content(data):
    items = data.get('items', [])

    context = {
        'full_name': data.get('full_name', 'not specified'),
        'phone_number': data.get('phone_number', 'not specified'),
        'address': data.get('address', 'not specified'),
        'email': data.get('email'),
        'items': items,
        'comment': data.get('comment', 'not specified')
    }

    html_message = render_to_string('emails/new_order.html', context)

    if items:
        products_str = "\n".join(f"- {item}" for item in items)
    else:
        products_str = "Нет товаров"

    text_message = (
        f"Поступил новый заказ от {context['full_name']}.\n"
        f"Телефон: {context['phone_number']}\n"
        f"Адрес: {context['address']}\n"
        f"Продукты:\n{products_str}"
    )

    return text_message, html_message

from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_202_ACCEPTED
from orders.serializers import OrderSerializer


class SendOrderView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'detail': 'Invalid request data', 'errors': serializer.errors},
                status=HTTP_400_BAD_REQUEST,
            )

        data = serializer.validated_data

        products_list = data.get('products', [])
        products_str = "\n".join([f"- {item}" for item in products_list]) if products_list else "Нет товаров"

        subject = "Новый заказ"
        message = f"""
Поступил новый заказ от {data.get('full_name', 'неизвестно')}.
Телефон: {data.get('phone_number', 'не указано')}
Адрес: {data.get('address', 'не указано')}
Продукты:
{products_str}
        """

        try:
            send_mail(
                subject=subject,
                message=message.strip(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.HR_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            return Response(
                {'detail': 'Ошибка при отправке письма', 'error': str(e)},
                status=HTTP_400_BAD_REQUEST
            )

        return Response({'detail': 'Спасибо! Ваш заказ оформлен. Скоро наши менеджеры свяжутся с вами.'}, status=HTTP_202_ACCEPTED)

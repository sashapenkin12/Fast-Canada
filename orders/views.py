from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_202_ACCEPTED
from orders.serializers import OrderSerializer
from orders.services.email_content import get_order_email_content


class SendOrderView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'detail': 'Invalid request data', 'errors': serializer.errors},
                status=HTTP_400_BAD_REQUEST,
            )

        data = serializer.validated_data
        subject = "Новый заказ"

        text_message, html_message = get_order_email_content(data)

        try:
            send_mail(
                subject=subject,
                message=text_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.HR_EMAIL],
                html_message=html_message,
                fail_silently=False,
            )
        except Exception as e:
            return Response(
                {'detail': 'Ошибка при отправке письма', 'error': str(e)},
                status=HTTP_400_BAD_REQUEST
            )

        return Response({'detail': 'Спасибо! Ваш заказ оформлен. Скоро наши менеджеры свяжутся с вами.'}, status=HTTP_202_ACCEPTED)

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_202_ACCEPTED
from rest_framework.views import APIView

from orders.serializers import OrderSerializer


class SendOrderView(APIView):
    def post(self, request, *args, **kwargs) -> Response:
        serializer = OrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'detail': 'Invalid request data', 'errors': serializer.errors},
                status=HTTP_400_BAD_REQUEST,
            )
        # Логика отправки по e-mail
        return Response(
            {'detail': 'Order successfully sent.'},
            status=HTTP_202_ACCEPTED,
        )

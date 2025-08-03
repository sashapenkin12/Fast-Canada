from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from cart.serializers import CartItemSerializer
from household_chemicals.models import ChemicalProduct


class CartView(APIView):
    def get(self, request):
        cart = request.session.get('cart', [])
        return CartItemSerializer(cart) if cart else Response(cart)


class AddItemView(APIView):
    def post(self, request):
        product_id = request.data.get('product')
        item_data = request.data.copy()

        product = ChemicalProduct.objects.get(id=product_id)
        item_data['product'] = product

        cart = request.session.get(settings.CART_SESSION_ID, [])
        item_data['id'] = len(cart) + 1

        cart_item = CartItemSerializer(data=item_data)
        if not cart_item.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Invalid request data.')

        cart.append(cart_item.data)

        request.session[settings.CART_SESSION_ID] = cart
        return Response(
            {'detail': 'Successfully added item to the cart.'},
            status=status.HTTP_201_CREATED,
        )


class DeleteItemView(APIView):
    def delete(self, request, item_id):
        cart = request.session.get(settings.CART_SESSION_ID, [])
        cart = [cart_item for cart_item in cart if cart.get('id') != item_id]
        request.session[settings.CART_SESSION_ID] = cart
        return Response({'detail': 'Item removed'}, status=status.HTTP_204_NO_CONTENT)


class DecreaseItemCountView(APIView):
    def patch(self, request, item_id: int) -> Response:
        cart: list[dict] = request.session.get(settings.CART_SESSION_ID, [])
        if not cart:
            return Response(
                {'detail': 'Cart item not found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        for cart_item in cart:
            if cart_item.get('id') == item_id:
                if cart_item['count'] == 1:
                    cart.remove(cart_item)
                else:
                    cart_item['count'] -= 1
        request.session[settings.CART_SESSION_ID] = cart
        return Response({'detail': 'Item count decreased'}, status=status.HTTP_200_OK)


class IncreaseItemCountView(APIView):
    def patch(self, request, item_id: int) -> Response:
        cart: list[dict] = request.session.get(settings.CART_SESSION_ID, [])
        if not cart:
            return Response(
                {'detail': 'Cart item not found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        for cart_item in cart:
            if cart_item.get('id') == item_id:
                if cart_item['count'] == 1:
                    cart.remove(cart_item)
                else:
                    cart_item['count'] += 1
        request.session[settings.CART_SESSION_ID] = cart
        return Response({'detail': 'Item count decreased'}, status=status.HTTP_200_OK)

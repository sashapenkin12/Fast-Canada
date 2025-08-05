from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .serializers import CartItemSerializer
from .services import CartManager, SessionCartStorage

class CartManagerMixin:
    @staticmethod
    def get_cart_manager(request: Request) -> CartManager:
        return CartManager(
            SessionCartStorage(
                request.session,
                settings.CART_SESSION_ID,
            ),
        )

class CartViewSet(ViewSet, CartManagerMixin):
    def list(self, request: Request) -> Response:
        """
        GET /cart/

        Retrieve current list of cart items by session ID.

        Args:
            request: Current HTTP request.

        Returns:
            Response: List of cart items.
        """

        cart = request.session.get(settings.CART_SESSION_ID, [])
        serializer = CartItemSerializer(cart, many=True)
        return Response(serializer.data)

    def create(self, request: Request) -> Response:
        """
        Add a new cart item.

        Args:
            request: Current HTTP request.

        Returns:
            Response: Response with 200 status code if data is valid, else 400
        """
        item_data = request.data.copy()
        try:
            with self.get_cart_manager(request) as cart:
                cart.add_to_cart(item_data)
        except ValidationError as exception:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'detail': exception.detail},
            )

        return Response(
            {'detail': 'Successfully added item to the cart.'},
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request: Request, pk: int) -> Response:
        """
        Delete a cart item.

        Args:
            request: Current HTTP request.
            pk: ID of the cart item, which needs to be deleted.

        Returns:
            Response: Response with 204 status code.
        """
        print(type(pk))
        with self.get_cart_manager(request) as cart:
            cart.remove_from_cart(pk)

        return Response(
            {'detail': 'Item removed'},
            status=status.HTTP_204_NO_CONTENT,
        )

    def increase(self, request: Request, pk: int):
        """
        Increase a count of the cart item.

        Args:
            request: Current HTTP request.
            pk: ID of the cart item, which count needs to be increased.

        Returns:
            Response: Response with 200 status code if item exists, else 404.
        """
        try:
            with self.get_cart_manager(request) as cart:
                cart.update_quantity(item_id=pk, delta=1)
        except ValidationError as exception:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'detail': exception.detail},
            )
        return Response(
            {'detail': 'Item count increased.'},
            status=status.HTTP_200_OK,
        )

    def decrease(self, request: Request, pk: int):
        """
        Decrease a count of the cart item.

        Args:
            request: Current HTTP request.
            pk: ID of the cart item, which needs to be deleted.

        Returns:
            Response: Response with 200 status code if item exists, else 404.
        """

        try:
            with self.get_cart_manager(request) as cart:
                cart.update_quantity(item_id=pk, delta=-1)
        except ValidationError as exception:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'detail': exception.detail},
            )
        return Response(
            {'detail': 'Item count decreased.'},
            status=status.HTTP_200_OK,
        )

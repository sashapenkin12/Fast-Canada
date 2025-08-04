from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .serializers import CartItemSerializer
from .services import CartManager


class CartView(APIView):
    """
    Cart View for retrieving current list of cart items

    Methods:
        get: Claims GET requests.
    """
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Retrieve current list of cart items by session ID.

        Args:
            request: Current HTTP request.

        Returns:
            Response: List of cart items.
        """
        cart = request.session.get(settings.CART_SESSION_ID, [])
        serializer = CartItemSerializer(cart, many=True)
        return Response(serializer.data)


class AddItemView(APIView):
    """
    Cart View for adding a new item to the cart.

    Methods:
        post: Claims POST requests.
    """
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Add a new cart item.

        Args:
            request: Current HTTP request.

        Returns:
            Response: Response with 200 status code if data is valid, else 400
        """
        item_data = request.data.copy()
        cart = CartManager(request.session, settings.CART_SESSION_ID)
        try:
            cart.add_to_cart(item_data)
        except ValidationError as exception:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=exception.detail,
            )
        cart.commit()
        return Response(
            {'detail': 'Successfully added item to the cart.'},
            status=status.HTTP_201_CREATED,
        )


class DeleteItemView(APIView):
    """
    Cart View for deleting an item from the cart.

    Methods:
        delete: Claims DELETE requests.
    """
    def delete(self, request: Request, item_id: int) -> Response:
        """
        Delete a cart item.

        Args:
            request: Current HTTP request.
            item_id: ID of the cart item, which needs to be deleted.

        Returns:
            Response: Response with 204 status code.
        """
        cart = CartManager(request.session, settings.CART_SESSION_ID)
        cart.remove_from_cart(item_id)
        cart.commit()
        return Response(
            {'detail': 'Item removed'},
            status=status.HTTP_204_NO_CONTENT,
        )


class DecreaseItemCountView(APIView):
    """
    Cart View for decreasing an amount of items in the cart.

    Methods:
        patch: Claims PATCH requests.
    """
    def patch(self, request: Request, item_id: int) -> Response:
        """
        Decrease a count of the cart item.

        Args:
            request: Current HTTP request.
            item_id: ID of the cart item, which needs to be deleted.

        Returns:
            Response: Response with 200 status code if item exists, else 404.
        """
        cart = CartManager(request.session, settings.CART_SESSION_ID)
        try:
            cart.update_quantity(item_id=item_id, delta=-1)
        except ValidationError as exception:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data=exception.detail,
            )
        cart.commit()
        return Response(
            {'detail': 'Item count decreased.'},
            status=status.HTTP_200_OK,
        )


class IncreaseItemCountView(APIView):
    """
    Cart View for increasing an amount of items in the cart.

    Methods:
        patch: Claims PATCH requests.
    """
    def patch(self, request, item_id: int) -> Response:
        """
        Increase a count of the cart item.

        Args:
            request: Current HTTP request.
            item_id: ID of the cart item, which needs to be deleted.

        Returns:
            Response: Response with 200 status code if item exists, else 404.
        """
        cart = CartManager(request.session, settings.CART_SESSION_ID)
        try:
            cart.update_quantity(item_id=item_id, delta=1)
        except ValidationError as exception:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data=exception.detail,
            )
        cart.commit()
        return Response(
            {'detail': 'Item count increased.'},
            status=status.HTTP_200_OK,
        )

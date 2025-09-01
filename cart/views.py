"""
Views for cart app.
"""

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status


from .serializers import CartItemSerializer, AddCartItemSerializer
from .services import CartManager, SessionCartStorage
from .paginations import CartPagination

class CartManagerMixin:
    """
    Mixin for CartManager access.

    Methods:
        get_cart_manager: Retrieve cart manager by current request.
    """
    @staticmethod
    def get_cart_manager(request: Request) -> CartManager:
        """
        Retrieve cart manager by current request.

        Args:
            request: Current HTTP request.

        Returns:
            CartManager: Cart manager.
        """
        return CartManager(
            storage=SessionCartStorage(
                request.session,
                settings.CART_SESSION_ID,
            ),
            request=request,
        )


class CartViewSet(ViewSet, CartManagerMixin):
    """
    ViewSet for working with cart.

    Attributes:
        pagination_class: Class for paginate cart items.
    """
    pagination_class = CartPagination

    @swagger_auto_schema(
        operation_summary="Get cart items",
        responses={200: CartItemSerializer(many=True)},
    )
    def list(self, request: Request) -> Response:
        """
        GET /api/cart/

        Retrieve current list of cart items by session ID.

        Args:
            request: Current HTTP request.

        Returns:
            Response: List of cart items.
        """

        cart: list = request.session.get(settings.CART_SESSION_ID, [])
        return Response(cart)

    @swagger_auto_schema(
        operation_summary="Add item to cart",
        request_body=AddCartItemSerializer,
        responses={
            201: openapi.Response(description="Created"),
            400: openapi.Response(description="Validation error"),
        },
    )
    def create(self, request: Request) -> Response:
        """
        POST /api/cart/add/

        Add a new cart item.

        Args:
            request: Current HTTP request.

        Returns:
            Response: Response with 201 status code if data is valid, else 400.
        """
        item_data: dict = request.data.copy()
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

    @swagger_auto_schema(
        operation_summary="Delete item from cart",
        responses={
            204: openapi.Response(description="No content"),
            404: openapi.Response(description="Not found"),
        },
    )
    def destroy(self, request: Request, pk: int) -> Response:
        """
        DELETE /api/cart/remove/<int:pk>/

        Delete a cart item.

        Args:
            request: Current HTTP request.
            pk: ID of the cart item, which needs to be deleted.

        Returns:
            Response: Response with 204 status code.
        """
        try:
            with self.get_cart_manager(request) as cart:
                cart.remove_from_cart(pk)
        except ValidationError as exception:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'detail': exception.detail},
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_summary="Increase item count",
        responses={
            200: openapi.Response(description="Item count increased"),
            404: openapi.Response(description="Not found"),
        },
    )
    def increase(self, request: Request, pk: int):
        """
        PATCH /api/cart/increase/<int:pk>/

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

    @swagger_auto_schema(
        operation_summary="Decrease item count",
        responses={
            200: openapi.Response(description="Item count decreased"),
            404: openapi.Response(description="Not found"),
        },
    )
    def decrease(self, request: Request, pk: int):
        """
        PATCH /api/cart/decrease/<int:pk>/

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

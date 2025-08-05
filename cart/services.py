"""
Services for cart app.
"""

from abc import ABC, abstractmethod
from typing import Callable, Optional

from rest_framework.exceptions import ValidationError

from .crud import get_product_by_id
from .serializers import CartProductSerializer, CartItemSerializer

class CartStorage(ABC):
    """
    Cart storage abstraction.

    Methods:
        load: Load storage.
        save: Save changes in storage.
    """
    @abstractmethod
    def load(self) -> list[dict]:
        """
        Load storage serialized object.

        Returns:
            list[dict]: Serialized python object for cart serving.
        """
        pass

    @abstractmethod
    def save(self, cart: list[dict]) -> None:
        """
        Save changes in serialized object to storage.

        Args:
            cart: Serialized python object with changes.
        """
        pass


class SessionCartStorage(CartStorage):
    """
    Cart storage realization with Django session.
    """
    def __init__(self, session: dict, session_key: str) -> None:
        """
        Init a session storage.

        Args:
            session: Current request session.
            session_key: Cart session key.
        """
        self.session = session
        self.session_key = session_key

    def load(self) -> list[dict]:
        """
        Load current session cart.

        Returns:
            list[dict]: Current cart.
        """
        return self.session.get(self.session_key, [])

    def save(self, cart: list[dict]) -> None:
        """
        Save changed cart to session.

        Args:
            cart: Modified cart.
        """
        self.session[self.session_key] = cart
        self.session.modified = True


class CartManager:
    """
    Manager for working with cart.
    """
    def __init__(self, storage: CartStorage):
        self.storage = storage

    def __enter__(self):
        self.cart = self.storage.load()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if not exc_type:
            self.storage.save(self.cart)
            return True
        return False

    def add_to_cart(self, item_data: dict) -> None:
        """
        Add item to the cart.

        Args:
            item_data: Item data.

        Raises:
            ValidationError: If data isn't matching structure.
        """
        item_data.setdefault('count', 1)
        product_id = item_data.get('product')
        if not product_id:
            raise ValidationError(detail='Product ID is required')
        product = get_product_by_id(product_id)
        product_data = CartProductSerializer(product).data

        if self.cart:
            duplicate_index = check_duplicate(self.cart, product_data['title'])
            if isinstance(duplicate_index, int):
                increment_item_count(self.cart, duplicate_index)
                return

        item_data['id'] = max([cart_item['id'] for cart_item in self.cart], default=0) + 1
        item_data['product'] = product_data

        cart_item = CartItemSerializer(data=item_data)
        if not cart_item.is_valid():
            raise ValidationError(detail=f'Invalid request data: {cart_item.errors}')

        self.cart.append(cart_item.data)

    def remove_from_cart(self, item_id: int) -> None:
        """
        Remove item from cart by ID.

        Args:
            item_id: Item ID.
        """
        for cart_item in self.cart:
            if cart_item.get('id') == item_id:
                self.cart.remove(cart_item)
                break

    def update_quantity(self, item_id: int, delta: int) -> None:
        if item_id not in [cart_item['id'] for cart_item in self.cart]:
            raise ValidationError(detail='Cart item not found.')
        apply_item_delta(
            cart=self.cart,
            item_id=item_id,
            delta=delta,
            on_zero=remove_if_zero,
        )


def increment_item_count(cart: list, index: int) -> None:
    """
    Increment item count in the cart.

    Args:
        cart: Current cart.
        index: Item cart index.
    """
    cart[index]['count'] += 1


def check_duplicate(cart: list, product_title: str) -> Optional[int]:
    """
    Check cart on duplicates. If found, returns index.

    Args:
        cart: Current cart.
        product_title: Product title.

    Returns:
        Optional[int]: If found, returns index, else None
    """
    for index, cart_item in enumerate(cart):
        if product_title == cart_item['product']['title']:
            return index


def remove_if_zero(cart: list, cart_item: dict) -> None:
    """
    Specifies actions for item count equals 0 scenario.

    Args:
        cart: Current cart.
        cart_item: Cart item, which count is equals 0.
    """
    cart.remove(cart_item)


def apply_item_delta(
        cart: list,
        item_id: int,
        delta: int,
        on_zero: Callable[[list, dict], None] = None
):
    """
    Specifies actions for item count equals 0 scenario.

    Args:
        cart: Current cart.
        item_id: Item for changing.
        delta: Difference between new value and old value.
        on_zero: Action for objects, which count equals zero.
    """
    for cart_item in cart:
        if cart_item.get('id') == item_id:
            cart_item['count'] += delta
            if cart_item['count'] == 0 and on_zero:
                on_zero(cart, cart_item)
            break

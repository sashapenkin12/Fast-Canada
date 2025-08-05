from abc import ABC, abstractmethod
from typing import Callable, Optional

from rest_framework.exceptions import ValidationError

from .crud import get_product_by_id
from .serializers import CartProductSerializer, CartItemSerializer

class CartStorage(ABC):
    @abstractmethod
    def load(self) -> list[dict]:
        pass

    @abstractmethod
    def save(self, cart: list[dict]) -> None:
        pass


class SessionCartStorage(CartStorage):
    def __init__(self, session: dict, session_key: str) -> None:
        self.session = session
        self.session_key = session_key

    def load(self) -> list[dict]:
        return self.session.get(self.session_key, [])

    def save(self, cart: list[dict]) -> None:
        self.session[self.session_key] = cart
        self.session.modified = True


class CartManager:
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

        add_cart_item(
            cart_item=cart_item.data,
            cart=self.cart,
        )

    def remove_from_cart(self, item_id: int) -> None:
        for cart_item in self.cart:
            if cart_item.get('id') == item_id:
                self.cart.remove(cart_item)

    def update_quantity(self, item_id: int, delta: int) -> None:
        if item_id not in [cart_item['id'] for cart_item in self.cart]:
            raise ValidationError(detail='Cart item not found.')
        apply_item_delta(
            cart=self.cart,
            item_id=item_id,
            delta=delta,
            on_zero=remove_if_zero,
        )


def increment_item_count(cart: list, index: int):
    cart[index]['count'] += 1


def check_duplicate(cart: list, product_title: str) -> Optional[int]:
    for index, cart_item in enumerate(cart):
        if product_title == cart_item['product']['title']:
            return index


def add_cart_item(
        cart_item: dict,
        cart: list[dict],
):
    cart.append(cart_item)


def remove_if_zero(cart: list, cart_item: dict):
    cart.remove(cart_item)


def apply_item_delta(
        cart: list,
        item_id: int,
        delta: int,
        on_zero: Callable[[list, dict], None] = None
):
    for cart_item in cart:
        if cart_item.get('id') == item_id:
            cart_item['count'] += delta
            if cart_item['count'] == 0 and on_zero:
                on_zero(cart, cart_item)
            break

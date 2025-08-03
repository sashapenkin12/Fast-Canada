"""
Pagination classes for paginated responses.
"""

from rest_framework.pagination import PageNumberPagination


class CartPagination(PageNumberPagination):
    """
    Pagination class for paginated cart items representation.

    Attributes:
        page_size: Default size of the page.
    """
    page_size = 5

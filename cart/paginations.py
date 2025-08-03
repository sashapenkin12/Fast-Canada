from rest_framework.pagination import PageNumberPagination


class CartPagination(PageNumberPagination):
    page_size = 5

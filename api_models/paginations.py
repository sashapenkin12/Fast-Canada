from rest_framework.pagination import PageNumberPagination

class VacancyPagination(PageNumberPagination):
    page_size = 8

class ServicePagination(PageNumberPagination):
    page_size = 5

class BlogPostPagination(PageNumberPagination):
    page_size = 9

class ProductPagination(PageNumberPagination):
    page_size = 5

class FAQPagination(PageNumberPagination):
    page_size = 4
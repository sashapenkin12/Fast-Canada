from django.urls import path
from .views import (
    ServiceViewSet, BrandViewSet, BlogPostViewSet, ContactViewSet,
    CityViewSet, LocationViewSet, AboutViewSet, BlogImageViewSet,
    CaseStudyViewSet, ProductViewSet, VacancyViewSet, VacancyApplicationViewSet,
    send_email_view, send_to_housecall, FAQViewSet
)

urlpatterns = [
    # Services
    path('services/', ServiceViewSet.as_view({'get': 'list'}), name='service-list'),
    path('services/<int:pk>/', ServiceViewSet.as_view({'get': 'retrieve'}), name='service-detail'),

    # Products
    path('products/', ProductViewSet.as_view({'get': 'list'}), name='product-list'),
    path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve'}), name='product-detail'),

    # Brands
    path('brands/', BrandViewSet.as_view({'get': 'list'}), name='brand-list'),
    path('brands/<int:pk>/', BrandViewSet.as_view({'get': 'retrieve'}), name='brand-detail'),

    # Blog
    path('blog/', BlogPostViewSet.as_view({'get': 'list'}), name='blog-list'),
    path('blog/<int:pk>/', BlogPostViewSet.as_view({'get': 'retrieve'}), name='blog-detail'),

    # Blog images
    path('blog-posts/<int:blog_post_id>/images/', BlogImageViewSet.as_view({'get': 'list'}), name='blogimage-list'),
    path('blog-posts/<int:blog_post_id>/images/<int:pk>/', BlogImageViewSet.as_view({'get': 'retrieve'}), name='blogimage-detail'),

    # Contact
    path('contact/', ContactViewSet.as_view({'get': 'list', 'post': 'create'}), name='contact'),

    # Cities
    path('cities/', CityViewSet.as_view({'get': 'list'}), name='city-list'),
    path('cities/<int:pk>/', CityViewSet.as_view({'get': 'retrieve'}), name='city-detail'),

    # Locations
    path('locations/', LocationViewSet.as_view({'get': 'list'}), name='location-list'),
    path('locations/<int:pk>/', LocationViewSet.as_view({'get': 'retrieve'}), name='location-detail'),

    # About
    path('about/', AboutViewSet.as_view({'get': 'list'}), name='about-list'),
    path('about/<int:pk>/', AboutViewSet.as_view({'get': 'retrieve'}), name='about-detail'),

    # Case studies
    path('casestudies/', CaseStudyViewSet.as_view({'get': 'list'}), name='casestudy-list'),
    path('casestudies/<int:pk>/', CaseStudyViewSet.as_view({'get': 'retrieve'}), name='casestudy-detail'),

    # Vacancies
    path('vacancies/', VacancyViewSet.as_view({'get': 'list', 'post': 'create'}), name='vacancy-list'),
    path('vacancies/<int:pk>/', VacancyViewSet.as_view({'get': 'retrieve'}), name='vacancy-detail'),

    # Vacancy Applications
    path('vacancy-applications/', VacancyApplicationViewSet.as_view({'get': 'list', 'post': 'create'}), name='vacancy-application-list'),
    path('vacancy-applications/<int:pk>/', VacancyApplicationViewSet.as_view({'get': 'retrieve'}), name='vacancy-application-detail'),

    # FAQ
    path('faqs/', FAQViewSet.as_view({'get': 'list'}), name='faq-list'),
    path('faqs/<int:pk>/', FAQViewSet.as_view({'get': 'retrieve'}), name='faq-detail'),

    # Custom views
    path('send-email/', send_email_view, name='send_email'),
    path('send-to-housecall/', send_to_housecall, name='send_to_housecall'),
]

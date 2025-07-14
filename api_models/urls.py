from django.urls import path
from .views import (
    ServiceViewSet, BrandViewSet, BlogPostViewSet, ContactViewSet,
    CityViewSet, LocationViewSet, AboutViewSet, BlogImageViewSet,
    CaseStudyViewSet, ProductViewSet, VacancyViewSet, VacancyApplicationViewSet,
    send_email_view, send_to_housecall, FAQViewSet, BrandHeaderViewSet
)

urlpatterns = [
    # Services
    path('services/', ServiceViewSet.as_view({'get': 'list'}), name='service-list'),
    path('services/<slug:slug>/', ServiceViewSet.as_view({'get': 'retrieve'}), name='service-detail'),

    # Products
    path('products/', ProductViewSet.as_view({'get': 'list'}), name='product-list'),
    path('products/<slug:slug>/', ProductViewSet.as_view({'get': 'retrieve'}), name='product-detail'),

    # Brands
    path('brands/', BrandViewSet.as_view({'get': 'list'}), name='brand-list'),
    path('brands/<slug:slug>/', BrandViewSet.as_view({'get': 'retrieve'}), name='brand-detail'),
    path('brand-headers/', BrandHeaderViewSet.as_view({'get': 'list'}), name='brand-header-list'),

    # Blog
    path('blog/', BlogPostViewSet.as_view({'get': 'list'}), name='blog-list'),
    path('blog/<slug:slug>/', BlogPostViewSet.as_view({'get': 'retrieve'}), name='blog-detail'),

    # Blog images
    path('blog-posts/<slug:blog_post_slug>/images/', BlogImageViewSet.as_view({'get': 'list'}), name='blogimage-list'),
    path('blog-posts/<slug:blog_post_slug>/images/<slug:slug>/', BlogImageViewSet.as_view({'get': 'retrieve'}), name='blogimage-detail'),

    # Contact
    path('contact/', ContactViewSet.as_view({'get': 'list', 'post': 'create'}), name='contact'),

    # Cities
    path('cities/', CityViewSet.as_view({'get': 'list'}), name='city-list'),
    path('cities/<slug:slug>/', CityViewSet.as_view({'get': 'retrieve'}), name='city-detail'),

    # Locations
    path('locations/', LocationViewSet.as_view({'get': 'list'}), name='location-list'),
    path('locations/<slug:slug>/', LocationViewSet.as_view({'get': 'retrieve'}), name='location-detail'),

    # About
    path('about/', AboutViewSet.as_view({'get': 'list'}), name='about-list'),

    # Case studies
    path('casestudies/', CaseStudyViewSet.as_view({'get': 'list'}), name='casestudy-list'),
    path('casestudies/<slug:slug>/', CaseStudyViewSet.as_view({'get': 'retrieve'}), name='casestudy-detail'),

    # Vacancies
    path('vacancies/', VacancyViewSet.as_view({'get': 'list', 'post': 'create'}), name='vacancy-list'),
    path('vacancies/<slug:slug>/', VacancyViewSet.as_view({'get': 'retrieve'}), name='vacancy-detail'),

    # Vacancy Applications
    path('vacancy-applications/', VacancyApplicationViewSet.as_view({'get': 'list', 'post': 'create'}), name='vacancy-application-list'),
    path('vacancy-applications/<slug:slug>/', VacancyApplicationViewSet.as_view({'get': 'retrieve'}), name='vacancy-application-detail'),

    # FAQ
    path('faqs/', FAQViewSet.as_view({'get': 'list'}), name='faq-list'),
    path('faqs/<slug:slug>/', FAQViewSet.as_view({'get': 'retrieve'}), name='faq-detail'),

    # Custom views
    path('send-email/', send_email_view, name='send_email'),
    path('send-to-housecall/', send_to_housecall, name='send_to_housecall'),
]

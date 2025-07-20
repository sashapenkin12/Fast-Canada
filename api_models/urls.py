from django.urls import path
from .views import (
    RepairViewSet, InstallationViewSet, BrandViewSet, BlogPostViewSet, ContactViewSet,
    CityViewSet, LocationViewSet, AboutViewSet, BlogImageViewSet, ServicesByCityHeaderViewSet,
    CaseStudyViewSet, ProductViewSet, VacancyViewSet, VacancyApplicationViewSet,
    send_email_view, send_to_housecall, FAQViewSet , BrandHeaderViewSet, GuaranteeViewSet,
    RepairHeaderViewSet, InstallationHeaderViewSet, ServicesByCityViewSet, PromotionViewSet,
    CombinedServiceHeaderViewSet, ServicesByCityHeaderSlugViewSet, CityHeaderViewSet
)

urlpatterns = [
    # Guarantees
    path('guarantees/', GuaranteeViewSet.as_view({'get': 'list'}), name='guarantee-list'),
    path('guarantees/<int:pk>/', GuaranteeViewSet.as_view({'get': 'retrieve'}), name='guarantee-detail'),

    path('promotions/', PromotionViewSet.as_view({'get': 'list'}), name='promotion-list'),

    # Repairs
    path('repairs/', RepairViewSet.as_view({'get': 'list'}), name='repair-list'),
    path('repairs/<slug:slug>/', RepairViewSet.as_view({'get': 'retrieve'}), name='repair-detail'),
    path('services-by-city/<str:city_slug>/', ServicesByCityViewSet.as_view({'get': 'list_services'}),
         name='services-by-city'),

    # Installations
    path('installations/', InstallationViewSet.as_view({'get': 'list'}), name='installation-list'),
    path('installations/<slug:slug>/', InstallationViewSet.as_view({'get': 'retrieve'}), name='installation-detail'),

    # Headers
    path('repair-headers/', RepairHeaderViewSet.as_view({'get': 'list'}), name='repair-header-list'),
    path('installation-headers/', InstallationHeaderViewSet.as_view({'get': 'list'}), name='installation-header-list'),
    path('services-by-city-header/<str:city_slug>/', ServicesByCityHeaderViewSet.as_view({'get': 'list_services'}),
         name='services-by-city-header'),
    path('services-combined-header/', CombinedServiceHeaderViewSet.as_view({'get': 'list'}), name='services-combined-header'),
    path('cities-headers/', CityHeaderViewSet.as_view({'get': 'list'}), name='city-header-list'),
    path('brand-headers/', BrandHeaderViewSet.as_view({'get': 'list'}), name='brand-header-list'),

    # Products
    path('products/', ProductViewSet.as_view({'get': 'list'}), name='product-list'),
    path('products/<slug:slug>/', ProductViewSet.as_view({'get': 'retrieve'}), name='product-detail'),

    # Brands
    path('brands/', BrandViewSet.as_view({'get': 'list'}), name='brand-list'),
    path('brands/<slug:slug>/', BrandViewSet.as_view({'get': 'retrieve'}), name='brand-detail'),

    # Blog
    path('blog/', BlogPostViewSet.as_view({'get': 'list'}), name='blog-list'),
    path('blog/<slug:slug>/', BlogPostViewSet.as_view({'get': 'retrieve'}), name='blog-detail'),

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
    path('vacancy-applications/<int:pk>/', VacancyApplicationViewSet.as_view({'get': 'retrieve'}), name='vacancy-application-detail'),

    # FAQ
    path('faqs/', FAQViewSet.as_view({'get': 'list'}), name='faq-list'),
    path('faqs/<int:pk>/', FAQViewSet.as_view({'get': 'retrieve'}), name='faq-detail'),

    # Custom views
    path('send-email/', send_email_view, name='send_email'),
    path('send-to-housecall/', send_to_housecall, name='send_to_housecall'),
]

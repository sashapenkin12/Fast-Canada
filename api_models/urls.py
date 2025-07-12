from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ServiceViewSet, BrandViewSet, BlogPostViewSet, ContactViewSet,
    CityViewSet, LocationViewSet, AboutViewSet, EmployeeViewSet,
    GalleryViewSet, CaseStudyViewSet, ProductViewSet, VacancyViewSet, VacancyApplicationViewSet, send_email_view,
    send_to_housecall
)

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='services')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'brands', BrandViewSet, basename='brands')
router.register(r'blog', BlogPostViewSet, basename='blog')
router.register(r'contact', ContactViewSet, basename='contact')
router.register(r'cities', CityViewSet, basename='cities')
router.register(r'locations', LocationViewSet, basename='locations')
router.register(r'about', AboutViewSet, basename='about')
router.register(r'employees', EmployeeViewSet, basename='employees')
router.register(r'gallery', GalleryViewSet, basename='gallery')
router.register(r'casestudies', CaseStudyViewSet, basename='casestudies')
router.register(r'vacancies', VacancyViewSet, basename='vacancy')
router.register(r'vacancy-applications', VacancyApplicationViewSet, basename='vacancy-application')

urlpatterns = [
    path('', include(router.urls)),
    path('send-email/', send_email_view, name='send_email'),
    path('send-to-housecall/', send_to_housecall, name='send_to_housecall'),
]

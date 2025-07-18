import logging

logger = logging.getLogger(__name__)

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import City, Location, Contact, Brand, BlogPost, About, CaseStudy, Product, BlogImage, \
    VacancyApplication, Vacancy, FAQ, Guarantee, Repair, Installation, Promotion
from .serializers import (
    CitySerializer, LocationSerializer, ContactSerializer, RepairSerializer, RepairHeaderSerializer, InstallationHeaderSerializer, CityHeaderSerializer,
    BrandSerializer, BlogPostSerializer, AboutSerializer, BlogImageSerializer, InstallationSerializer, PromotionSerializer, InstallationCombinedServiceHeaderSerializer,
    CaseStudySerializer, ProductSerializer, VacancyApplicationSerializer, VacancySerializer, FAQSerializer, BrandHeaderSerializer, GuaranteeSerializer, RepairCombinedServiceHeaderSerializer
)
from integrations.housecall import send_to_housecall_pro
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
import requests
from decouple import config
from .paginations import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
import logging


logger = logging.getLogger(__name__)


class CityHeaderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CityHeaderSerializer


class CombinedServiceHeaderViewSet(viewsets.ViewSet):
    def list(self, request):
        repairs = Repair.objects.all()
        installations = Installation.objects.all()

        repair_serializer = RepairCombinedServiceHeaderSerializer(repairs, many=True)
        installation_serializer = InstallationCombinedServiceHeaderSerializer(installations, many=True)

        services = {
            'repairs': repair_serializer.data,
            'installations': installation_serializer.data
        }
        return Response(services)


class ServicesByCityHeaderViewSet(viewsets.ViewSet):
    @action(detail=True, methods=['get'], url_path='services-by-city-header/(?P<city_slug>[^/.]+)')
    def list_services(self, request, city_slug):
        try:
            city = City.objects.get(slug=city_slug)
            repairs = Repair.objects.filter(available_in_cities=city)
            installations = Installation.objects.filter(available_in_cities=city)

            repair_serializer = RepairHeaderSerializer(repairs, many=True)
            installation_serializer = InstallationHeaderSerializer(installations, many=True)

            services = {
                'repairs': repair_serializer.data,
                'installations': installation_serializer.data
            }
            return Response(services)
        except City.DoesNotExist:
            return Response({'error': 'City not found'}, status=404)


class ServiceHeaderSlugViewSet(viewsets.ViewSet):
    def list(self, request):
        repairs = Repair.objects.all()
        installations = Installation.objects.all()

        repair_serializer = RepairHeaderSerializer(repairs, many=True)
        installation_serializer = InstallationHeaderSerializer(installations, many=True)

        services = {
            'repairs': repair_serializer.data,
            'installations': installation_serializer.data
        }
        return Response(services)


class ServicesByCityHeaderSlugViewSet(viewsets.ViewSet):
    @action(detail=True, methods=['get'], url_path='services-by-city-header/(?P<city_slug>[^/.]+)')
    def list_services(self, request, city_slug):
        try:
            city = City.objects.get(slug=city_slug)
            repairs = Repair.objects.filter(available_in_cities=city)
            installations = Installation.objects.filter(available_in_cities=city)

            repair_serializer = RepairHeaderSerializer(repairs, many=True)
            installation_serializer = InstallationHeaderSerializer(installations, many=True)

            services = {
                'repairs': repair_serializer.data,
                'installations': installation_serializer.data
            }
            return Response(services)
        except City.DoesNotExist:
            return Response({'error': 'City not found'}, status=404)


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer


class BlogPostPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 100


class VacancyPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100


class CaseStudyPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    pagination_class = BlogPostPagination

    def get_queryset(self):
        logger.info(f"Getting queryset for {self.__class__.__name__}")
        return super().get_queryset()


class ServicesByCityViewSet(viewsets.ViewSet):
    @action(detail=True, methods=['get'], url_path='services-by-city/(?P<city_slug>[^/.]+)')
    def list_services(self, request, city_slug):
        try:
            city = City.objects.get(slug=city_slug)
            repairs = Repair.objects.filter(available_in_cities=city)
            installations = Installation.objects.filter(available_in_cities=city)

            repair_serializer = RepairSerializer(repairs, many=True)
            installation_serializer = InstallationSerializer(installations, many=True)

            services = {
                'repairs': repair_serializer.data,
                'installations': installation_serializer.data
            }
            return Response(services)
        except City.DoesNotExist:
            return Response({'error': 'City not found'}, status=404)


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = 'slug'

    def get_queryset(self):
        logger.info(f"Getting queryset for {self.__class__.__name__}")
        return super().get_queryset()


class GuaranteeViewSet(viewsets.ModelViewSet):
    queryset = Guarantee.objects.all()
    serializer_class = GuaranteeSerializer


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    lookup_field = 'slug'

    def get_object(self):
        slug = self.kwargs.get(self.lookup_field)
        obj = self.queryset.get(slug=slug)
        self.check_object_permissions(self.request, obj)
        return obj


class RepairViewSet(viewsets.ModelViewSet):
    queryset = Repair.objects.all()
    serializer_class = RepairSerializer
    lookup_field = 'slug'


class InstallationViewSet(viewsets.ModelViewSet):
    queryset = Installation.objects.all()
    serializer_class = InstallationSerializer
    lookup_field = 'slug'


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save()
            try:
                send_to_housecall_pro(contact)
                contact.sent_to_crm = True
                contact.save()
                return Response({"message": "Application successfully sent to HouseCall Pro"},
                                status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": f"Error sending to CRM: {str(e)}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        logger.info(f"Getting queryset for {self.__class__.__name__}")
        return super().get_queryset()


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        logger.info(f"Getting queryset for {self.__class__.__name__}")
        return super().get_queryset()


class BrandHeaderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandHeaderSerializer


class RepairHeaderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Repair.objects.all()
    serializer_class = RepairHeaderSerializer


class InstallationHeaderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Installation.objects.all()
    serializer_class = InstallationHeaderSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        brand_slug = self.request.query_params.get('brand', None)
        if brand_slug:
            queryset = queryset.filter(brand__slug=brand_slug)
        return queryset


class BlogImageViewSet(viewsets.ModelViewSet):
    queryset = BlogImage.objects.all()
    serializer_class = BlogImageSerializer

    def get_queryset(self):
        logger.info(f"Getting queryset for {self.__class__.__name__}")
        if 'blog_post_id' in self.kwargs:
            try:
                blog_post_id = self.kwargs['blog_post_id']
                if not blog_post_id.isdigit():
                    logger.error(f"Invalid blog_post_id: {blog_post_id}")
                    return BlogImage.objects.none()
                return BlogImage.objects.filter(blog_post_id=blog_post_id)
            except Exception as e:
                logger.error(f"Error in BlogImageViewSet: {e}")
                return BlogImage.objects.none()
        return super().get_queryset()

    def perform_create(self, serializer):
        blog_post_id = self.kwargs.get('blog_post_id')
        if blog_post_id:
            blog_post = BlogPost.objects.get(id=blog_post_id)
            serializer.save(blog_post=blog_post)
        else:
            serializer.save()


class AboutViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer

    def get_queryset(self):
        logger.info(f"Getting queryset for {self.__class__.__name__}")
        return super().get_queryset()


class CaseStudyViewSet(viewsets.ModelViewSet):
    queryset = CaseStudy.objects.all()
    serializer_class = CaseStudySerializer
    lookup_field = 'slug'
    pagination_class = CaseStudyPagination

    def get_queryset(self):
        logger.info(f"Getting queryset for {self.__class__.__name__}")
        return super().get_queryset()


class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.filter(is_active=True)
    serializer_class = VacancySerializer
    lookup_field = 'slug'
    pagination_class = VacancyPagination

    def get_queryset(self):
        logger.info(f"Getting queryset for {self.__class__.__name__}")
        return super().get_queryset()


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    pagination_class = FAQPagination

    def get_queryset(self):
        logger.info(f"Getting queryset for {self.__class__.__name__}")
        content_type = self.request.query_params.get('content_type')
        object_id = self.request.query_params.get('object_id')
        queryset = self.queryset
        if content_type and object_id:
            from django.contrib.contenttypes.models import ContentType
            try:
                ct = ContentType.objects.get(model=content_type)
                queryset = queryset.filter(content_type=ct, object_id=object_id)
            except ContentType.DoesNotExist as e:
                logger.error(f"Error in FAQViewSet: {e}")
                queryset = queryset.none()
            except Exception as e:
                logger.error(f"Unexpected error in FAQViewSet: {e}")
                queryset = queryset.none()
        return queryset.order_by('order')

    def perform_create(self, serializer):
        content_type = self.request.query_params.get('content_type')
        object_id = self.request.query_params.get('object_id')
        if content_type and object_id:
            from django.contrib.contenttypes.models import ContentType
            ct = ContentType.objects.get(model=content_type)
            serializer.save(content_type=ct, object_id=object_id)
        else:
            serializer.save()


class VacancyApplicationViewSet(viewsets.ModelViewSet):
    queryset = VacancyApplication.objects.all()
    serializer_class = VacancyApplicationSerializer
    swagger_fake_view = True

    def get_queryset(self):
        logger.info(f"Getting queryset for {self.__class__.__name__}")
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        vacancy = serializer.validated_data['vacancy']
        subject = f"New Application for {vacancy.title}"
        message = (
            f"New application received:\n\n"
            f"Vacancy: {vacancy.title}\n"
            f"Name: {serializer.validated_data['name']}\n"
            f"Email: {serializer.validated_data['email']}\n"
            f"Phone: {serializer.validated_data['phone']}\n"
            f"Message: {serializer.validated_data['message']}\n"
        )
        if serializer.validated_data.get('resume'):
            message += f"Resume: Attached (see admin panel for download)"

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.HR_EMAIL],
            fail_silently=False,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()


def send_email_view(request):
    if request.method == 'POST':
        subject = 'Test email'
        message = 'This is a test message from your Django application.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['bloodyangel10k@gmail.com']
        send_mail(subject, message, from_email, recipient_list)
        return HttpResponse('Email sent!')
    return HttpResponse('Use a POST request to send.')


def send_to_housecall(request):
    if request.method == 'POST':
        url = 'https://api.housecallpro.com/endpoint'
        headers = {'Authorization': f'Bearer {config("HOUSECALL_API_KEY")}'}
        data = {'message': 'Test message'}
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            return HttpResponse(f'Sent: {response.text}')
        except requests.RequestException as e:
            return HttpResponse(f'Error: {str(e)}', status=500)
    return HttpResponse('Use a POST request.')

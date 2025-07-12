from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import City, Location, Service, Contact, Brand, BlogPost, About, Employee, Gallery, CaseStudy, Product, \
    VacancyApplication, Vacancy
from .serializers import (
    CitySerializer, LocationSerializer, ServiceSerializer, ContactSerializer,
    BrandSerializer, BlogPostSerializer, AboutSerializer, EmployeeSerializer,
    GallerySerializer, CaseStudySerializer, ProductSerializer, VacancyApplicationSerializer, VacancySerializer
)
from integrations.housecall import send_to_housecall_pro
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
import requests
from decouple import config


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = 'name'


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
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
                return Response({"message": "Заявка успешно отправлена в HouseCall Pro"},
                                status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": f"Ошибка отправки в CRM: {str(e)}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'slug'


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Product.objects.all()
        brand_slug = self.request.query_params.get('brand')
        if brand_slug:
            queryset = queryset.filter(brand__slug=brand_slug)
        return queryset


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'


class AboutViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer


class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class GalleryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer


class CaseStudyViewSet(viewsets.ModelViewSet):
    queryset = CaseStudy.objects.all()
    serializer_class = CaseStudySerializer
    lookup_field = 'slug'


class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.filter(is_active=True)
    serializer_class = VacancySerializer
    lookup_field = 'slug'


class VacancyApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = VacancyApplicationSerializer

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
            [settings.HR_EMAIL],  # Требуется настройка в settings.py
            fail_silently=False,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()


def send_email_view(request):
    if request.method == 'POST':
        subject = 'Тестовое письмо'
        message = 'Это тестовое сообщение от вашего Django-приложения.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['bloodyangel10k@gmail.com']
        send_mail(subject, message, from_email, recipient_list)
        return HttpResponse('Письмо отправлено!')
    return HttpResponse('Используйте POST-запрос для отправки.')


def send_to_housecall(request):
    if request.method == 'POST':
        url = 'https://api.housecallpro.com/endpoint'
        headers = {'Authorization': f'Bearer {config("HOUSECALL_API_KEY")}'}
        data = {'message': 'Тестовое сообщение'}
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            return HttpResponse(f'Отправлено: {response.text}')
        except requests.RequestException as e:
            return HttpResponse(f'Ошибка: {str(e)}', status=500)
    return HttpResponse('Используйте POST-запрос.')

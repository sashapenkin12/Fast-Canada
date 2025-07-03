from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    province = models.CharField(max_length=100, default="Онтарио")
    services = models.ManyToManyField('Service', related_name='cities')
    latitude = models.FloatField(help_text="Широта города (например, 43.6532 для Торонто)")
    longitude = models.FloatField(help_text="Долгота города (например, -79.3832 для Торонто)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, {self.province}"


class Location(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="locations")
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.city.name})"


class Service(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('repairs', 'Ремонт'),
        ('installations', 'Установка'),
    ]
    title = models.CharField(max_length=200, unique=True)
    type_service = models.CharField(choices=SERVICE_TYPE_CHOICES)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    short_description = models.TextField()
    full_description = models.TextField()
    icon = models.URLField(blank=True)
    image = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    faqs = GenericRelation('FAQ', related_query_name='service')

    def get_category(self):
        return 'Repairs' if self.title.startswith('repairs_') else 'Installations'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.get_title_display())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_title_display()


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    logo = models.ImageField("media/brands_images", blank=True)
    description = models.TextField()
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    faqs = GenericRelation('FAQ', related_query_name='brand')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    pros = models.TextField(blank=True, help_text="Список плюсов, разделённых переносом строки")
    cons = models.TextField(blank=True, help_text="Список минусов, разделённых переносом строки")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.brand.name}-{self.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand.name} - {self.name}"


class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('articles', 'Статьи'),
        ('lifehacks', 'Лайфхаки'),
        ('reviews', 'Обзоры'),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.URLField(blank=True)
    video_on_youtube = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    faqs = GenericRelation('FAQ', related_query_name='blog_post')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=70)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    description = models.TextField()
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_to_crm = models.BooleanField(default=False)
    faqs = GenericRelation('FAQ', related_query_name='contact')

    def __str__(self):
        return f"{self.name} - {self.email}"


class About(models.Model):
    mission = models.TextField(max_length=500)
    experience = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    faqs = GenericRelation('FAQ', related_query_name='about')

    def __str__(self):
        return "About Fast Canada"


class Employee(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    photo = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Gallery(models.Model):
    image = models.URLField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"


class CaseStudy(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    image = models.URLField(blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    faqs = GenericRelation('FAQ', related_query_name='case_study')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class FAQ(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    question = models.CharField(max_length=200)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0, help_text="Порядок отображения")

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['order']

    def __str__(self):
        return self.question


class Vacancy(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    salary = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class VacancyApplication(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Vacancy Application"
        verbose_name_plural = "Vacancy Applications"

    def __str__(self):
        return f"{self.name} - {self.vacancy.title}"

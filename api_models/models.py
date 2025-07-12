from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from ckeditor.fields import RichTextField


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    province = models.CharField(max_length=100, default="Ontario")
    services = models.ManyToManyField('Service', related_name='cities')
    latitude = models.FloatField(help_text="City latitude (e.g., 43.6532 for Toronto)")
    longitude = models.FloatField(help_text="City longitude (e.g., -79.3832 for Toronto)")
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.province}"

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"


class Location(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="locations")
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.city.name})"

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"


class Service(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('repairs', 'Repair'),
        ('installations', 'Installation'),
    ]
    title = models.CharField(max_length=200, unique=True)
    type_service = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    full_description = RichTextField(blank=True, null=True)
    icon = models.ImageField(upload_to='service_icon/', blank=True, null=True)
    image = models.ImageField(upload_to='service_image/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    faqs = GenericRelation('FAQ', related_query_name='service')

    def get_category(self):
        return 'Repairs' if self.title.lower().startswith('repairs_') else 'Installations'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = base_slug
            counter = 1
            while Service.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_type_service_display(self):
        return dict(self.SERVICE_TYPE_CHOICES).get(self.type_service, '')

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    logo = models.ImageField(upload_to='brands_images/', blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    faqs = GenericRelation('FAQ', related_query_name='brand')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = base_slug
            counter = 1
            while Brand.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"


class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = RichTextField(blank=True, null=True)
    pros = models.TextField(blank=True, help_text="List of pros, separated by new lines")
    cons = models.TextField(blank=True, help_text="List of cons, separated by new lines")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.brand.name}-{self.name}")
            self.slug = base_slug
            counter = 1
            while Product.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand.name} - {self.name}"


class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('articles', 'Articles'),
        ('lifehacks', 'Lifehacks'),
        ('reviews', 'Reviews'),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = RichTextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='blog_image/', blank=True, null=True)
    video_on_youtube = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    faqs = GenericRelation('FAQ', related_query_name='blog_post')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"


class Contact(models.Model):
    name = models.CharField(max_length=70)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    description = RichTextField(blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_to_crm = models.BooleanField(default=False)
    faqs = GenericRelation('FAQ', related_query_name='contact')

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"


class About(models.Model):
    mission = models.TextField(max_length=500)
    experience = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    faqs = GenericRelation('FAQ', related_query_name='about')

    def __str__(self):
        return "About Fast Canada"

    class Meta:
        verbose_name = "About"
        verbose_name_plural = "About Pages"


class Employee(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='employee_image/', blank=True, null=True)
    bio = models.TextField(blank=True)  # Can be replaced with RichTextField
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"


class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery_image/', blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"

    class Meta:
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"


class CaseStudy(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = RichTextField(blank=True, null=True)
    image = models.ImageField(upload_to='case_study_image/', blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    faqs = GenericRelation('FAQ', related_query_name='case_study')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = base_slug
            counter = 1
            while CaseStudy.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Case Study"
        verbose_name_plural = "Case Studies"


class FAQ(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    question = models.CharField(max_length=200)
    answer = models.TextField()  # Can be replaced with RichTextField
    order = models.PositiveIntegerField(default=0, help_text="Display order")

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['order']

    def __str__(self):
        return self.question


class Vacancy(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
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
            base_slug = slugify(self.title)
            self.slug = base_slug
            counter = 1
            while Vacancy.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
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
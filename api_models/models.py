from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError


class Promotion(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=150, null=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"
        ordering = ['-date']


class Guarantee(models.Model):
    full_text = RichTextField(help_text="Detailed guarantee text with formatting")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time of creation")

    class Meta:
        verbose_name = "Guarantee"
        verbose_name_plural = "Guarantees"
        ordering = ['-created_at']


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    province = models.CharField(max_length=100, default="Ontario")
    repairs = models.ManyToManyField('Repair', related_name='available_in_cities', blank=True)
    installations = models.ManyToManyField('Installation', related_name='available_in_cities', blank=True)
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


class Repair(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text="Title of the repair service (e.g., Repairs_HVAC)", null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, help_text="Unique slug generated from title")
    short_description = models.CharField(max_length=200, help_text="Short description of the repair service", blank=True, null=True)
    full_description = RichTextField(max_length=680, blank=True, null=True, help_text="Detailed description of the repair service")
    cart_description = models.CharField(max_length=128, help_text="Short description of the installation service", blank=True, null=True)
    icon = models.ImageField(upload_to='service_icon/', blank=True, null=True, help_text="Icon for the repair service")
    image = models.ImageField(upload_to='service_image/', blank=True, null=True, help_text="Image for the repair service")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time of creation")
    faqs = GenericRelation('FAQ', related_query_name='repair')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name or '')
            self.slug = base_slug
            counter = 1
            while Repair.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name or "Unnamed Repair"

    class Meta:
        verbose_name = "Repair"
        verbose_name_plural = "Repairs"
        ordering = ['-created_at']


class Installation(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text="Title of the installation service (e.g., Installations_AC)", null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, help_text="Unique slug generated from title")
    short_description = models.CharField(max_length=200, help_text="Short description of the installation service", blank=True, null=True)
    full_description = RichTextField(max_length=680, blank=True, null=True, help_text="Detailed description of the installation service")
    cart_description = models.CharField(max_length=128, help_text="Short description of the installation service", blank=True, null=True)
    icon = models.ImageField(upload_to='service_icon/', blank=True, null=True, help_text="Icon for the installation service")
    image = models.ImageField(upload_to='service_image/', blank=True, null=True, help_text="Image for the installation service")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time of creation")
    faqs = GenericRelation('FAQ', related_query_name='installation')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name or '')
            self.slug = base_slug
            counter = 1
            while Installation.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name or "Unnamed Installation"

    class Meta:
        verbose_name = "Installation"
        verbose_name_plural = "Installations"
        ordering = ['-created_at']


class Location(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="locations")
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    plase_id = models.CharField(max_length=100, null=True)
    latitude = models.FloatField(help_text="City latitude (e.g., 43.6532 for Toronto)", null=True)
    longitude = models.FloatField(help_text="City longitude (e.g., -79.3832 for Toronto)", null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Location.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.city.name})"


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    logo = models.ImageField(upload_to='brands_images/', blank=True, null=True)
    description = models.TextField(max_length=300, blank=True, null=True)
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
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('articles', 'Articles'),
        ('lifehacks', 'Lifehacks'),
        ('reviews', 'Reviews'),
    ]
    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=500, null=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = RichTextField(blank=True, null=True)
    text_for_cover = models.CharField(max_length=150, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    video_on_youtube = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    faqs = GenericRelation('FAQ', related_query_name='blog_post')

    def clean(self):
        super().clean()
        if self.pk and not BlogImage.objects.filter(blog_post=self).exists():
            raise ValidationError("A BlogPost must have at least one associated image.")

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


class BlogImage(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='blog_images/')  # РѕР±СЏР·Р°С‚РµР»СЊРЅРѕРµ РїРѕР»Рµ
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.blog_post.title}"

    class Meta:
        verbose_name = "Blog Image"
        verbose_name_plural = "Blog Images"


class Contact(models.Model):
    name = models.CharField(max_length=70, help_text="Full name of the contact (max 70 characters)")
    phone = models.CharField(max_length=20, blank=True, null=True, help_text="Phone number (e.g., +1 (123) 456-7890)")
    email = models.EmailField(unique=True, help_text="Email address for communication")
    address = models.TextField(help_text="Full address of the contact")
    description = models.TextField(blank=True, null=True, help_text="Detailed description or notes about the contact")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time of contact creation")
    sent_to_crm = models.BooleanField(default=False, help_text="Indicates if the contact was sent to CRM")
    status = models.CharField(max_length=20, choices=[('new', 'New'), ('processed', 'Processed'), ('closed', 'Closed')],
                              default='new', help_text="Status of the contact request")

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ['-created_at']


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


class CaseStudyImage(models.Model):
    case_study = models.ForeignKey('CaseStudy', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='case_study_images/', help_text="Image for the case study")
    caption = models.CharField(max_length=200, blank=True, null=True, help_text="Caption for the image")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time of image creation")

    def __str__(self):
        return f"Image for {self.case_study.title}"

    class Meta:
        verbose_name = "Case Study Image"
        verbose_name_plural = "Case Study Images"


class CaseStudy(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    short_description = models.TextField(max_length=129, null=True)
    description = models.TextField(max_length=180, null=True)
    image = models.ImageField(upload_to='case_study_image/', blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    video_on_youtube = models.URLField(blank=True, null=True)
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
    answer = RichTextField(blank=True, null=True)
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
    conditions = models.TextField(blank=True)
    location = models.ForeignKey(City, on_delete=models.CASCADE, related_name='vacancies', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    requirements = models.TextField(blank=True, null=True)

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

    class Meta:
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"


class VacancyApplication(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.vacancy.title}"

    class Meta:
        verbose_name = "Vacancy Application"
        verbose_name_plural = "Vacancy Applications"

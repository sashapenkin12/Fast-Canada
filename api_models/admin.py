from django.contrib import admin
from django.db import models
from ckeditor.widgets import CKEditorWidget
from .models import (
    City, Location, Service, Contact, Brand, BlogPost, BlogImage,
    About, CaseStudy, Vacancy, VacancyApplication, Product, FAQ
)


# --- Inline ---
class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 3


# --- City ---
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'province', 'created_at']
    search_fields = ['name']
    filter_horizontal = ['services']


# --- Location ---
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'address']
    search_fields = ['name', 'address']
    list_filter = ['city']


# --- Service ---
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['get_category', 'title', 'slug', 'created_at']
    search_fields = ['title', 'slug', 'full_description']
    list_filter = ['type_service']
    prepopulated_fields = {'slug': ('title',)}
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }

    def get_category(self, obj):
        return obj.get_category()

    get_category.short_description = 'Category'


# --- Contact ---
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'sent_to_crm', 'created_at', 'description', 'status', 'address']
    search_fields = ['name', 'email']
    list_filter = ['sent_to_crm']


# --- Brand ---
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}


# --- BlogPost ---
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    inlines = [BlogImageInline]
    list_display = ['title', 'slug', 'category', 'created_at']
    search_fields = ['title', 'slug', 'content']
    list_filter = ['category']
    prepopulated_fields = {'slug': ('title',)}
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }


# --- About ---
@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['id', 'mission', 'experience', 'created_at']
    search_fields = ['mission', 'experience']


# --- CaseStudy ---
@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'city', 'created_at']
    search_fields = ['title', 'slug', 'description']
    list_filter = ['city']
    prepopulated_fields = {'slug': ('title',)}


# --- Vacancy ---
@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_active', 'created_at', 'location', 'conditions']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['is_active']


# --- VacancyApplication ---
@admin.register(VacancyApplication)
class VacancyApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'vacancy', 'email', 'phone', 'created_at']
    list_filter = ['vacancy']


# --- Product ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['brand', 'name', 'description', 'updated_at', 'created_at']
    list_filter = ['brand']


# --- FAQ ---
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'content_object', 'question', 'answer', 'order']
    search_fields = ['question']

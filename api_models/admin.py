from django.contrib import admin
from .models import City, Location, Service, Contact, Brand, BlogPost, About, Employee, Gallery, CaseStudy, Vacancy, \
    VacancyApplication


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'province', 'created_at']
    search_fields = ['name']
    filter_horizontal = ['services']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'address']
    search_fields = ['name', 'address']
    list_filter = ['city']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['get_category', 'title', 'slug', 'created_at']
    search_fields = ['title', 'slug', 'short_description']
    list_filter = ['title']
    prepopulated_fields = {'slug': ('title',)}

    def get_category(self, obj):
        return obj.get_category()

    get_category.short_description = 'Category'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'city', 'service', 'location', 'sent_to_crm', 'created_at']
    search_fields = ['name', 'email']
    list_filter = ['sent_to_crm', 'city', 'service', 'location']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'category', 'created_at']
    search_fields = ['title', 'slug', 'content']
    list_filter = ['category']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at']
    search_fields = ['mission', 'experience']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'created_at']
    search_fields = ['name', 'bio']
    list_filter = ['position']


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'created_at']
    search_fields = ['description']


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'city', 'created_at']
    search_fields = ['title', 'slug', 'description']
    list_filter = ['city']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_active', 'created_at']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['is_active']


@admin.register(VacancyApplication)
class VacancyApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'vacancy', 'email', 'phone', 'created_at']
    list_filter = ['vacancy']

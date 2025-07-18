from django.contrib import admin
from .models import City, Location, Contact, Brand, BlogPost, About, CaseStudy, Vacancy, \
    VacancyApplication, Product, FAQ, BlogImage, Guarantee, Repair, Installation, Promotion
from ckeditor.widgets import CKEditorWidget
from django.db import models
from django.forms.models import BaseInlineFormSet


class BlogImageInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        total_forms = len([form for form in self.forms if not form.cleaned_data.get('DELETE', False) and form.cleaned_data.get('image')])
        if total_forms == 0:
            raise ValidationError("РќРµРѕР±С…РѕРґРёРјРѕ РґРѕР±Р°РІРёС‚СЊ С…РѕС‚СЏ Р±С‹ РѕРґРЅРѕ РёР·РѕР±СЂР°Р¶РµРЅРёРµ.")


class ProductInline(admin.TabularInline):
    model = Product
    extra = 5
    fields = ('name', 'description')


class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1
    min_num = 1
    validate_min = True


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'created_at')
    search_fields = ('title', 'description')


@admin.register(Guarantee)
class GuaranteeAdmin(admin.ModelAdmin):
    list_display = ('created_at',)
    search_fields = ('full_text', 'slug')
    list_filter = ('created_at',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'logo', 'description', 'created_at')
        }),
    )
    readonly_fields = ('created_at',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'created_at', 'updated_at')
    list_filter = ('brand',)
    fieldsets = (
        (None, {
            'fields': ('brand', 'name', 'slug', 'created_at', 'updated_at', 'description', 'image')
        }),
    )
    readonly_fields = ('slug', 'created_at', 'updated_at')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'slug', 'created_at', 'slug')
    search_fields = ('name', 'province')
    filter_horizontal = ('repairs', 'installations')

@admin.register(Repair)
class RepairAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'full_description')

@admin.register(Installation)
class InstallationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'full_description')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'longitude', 'latitude']
    search_fields = ['name', 'longitude', 'latitude']
    list_filter = ['city']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'sent_to_crm', 'created_at', 'description', 'status', 'address']
    search_fields = ['name', 'email']
    list_filter = ['sent_to_crm', ]


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    inlines = [BlogImageInline]
    list_display = ['title', 'slug', 'category', 'created_at', 'text_for_cover', 'short_description']
    search_fields = ['title', 'slug', 'content']
    list_filter = ['category']
    prepopulated_fields = {'slug': ('title',)}

    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['id', 'mission', 'experience', 'created_at']
    search_fields = ['mission', 'experience']


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'city', 'created_at']
    search_fields = ['title', 'slug', 'description']
    list_filter = ['city']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_active', 'created_at', 'location', 'conditions', 'requirements']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['is_active']


@admin.register(VacancyApplication)
class VacancyApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'vacancy', 'email', 'phone', 'created_at']
    list_filter = ['vacancy']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['content_type','content_type', 'content_object', 'question', 'answer', 'order']
    list_field = ['question']


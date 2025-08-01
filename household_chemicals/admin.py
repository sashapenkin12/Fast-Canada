from django.contrib import admin

from household_chemicals.models import ChemicalProduct

@admin.register(ChemicalProduct)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'full_description', 'price', 'is_available', 'image')
    search_fields = ('title', 'full_description')

from django.contrib import admin

from household_chemicals.models import ChemicalProduct

@admin.register(ChemicalProduct)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'price', 'is_available', 'image')
    search_fields = ('title', 'full_description')
    list_filter = ('is_available',)


    def short_description(self, obj):
        return obj.full_description[:50] + '...' \
            if len(obj.full_description) > 50 else obj.full_description

    short_description.short_description = 'Description'

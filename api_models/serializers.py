from rest_framework import serializers
from .models import City, Location, Service, Contact, Brand, BlogPost, About, Employee, Gallery, CaseStudy, Product, \
    VacancyApplication, Vacancy
from integrations.google_translate import translate_text


class ServiceSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    title = serializers.CharField(source='get_title_display')
    translated_short_description = serializers.SerializerMethodField()
    translated_full_description = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.get_category()

    def get_translated_short_description(self, obj):
        language = self.context['request'].query_params.get('language', 'en')
        return translate_text(obj.short_description, language)

    def get_translated_full_description(self, obj):
        language = self.context['request'].query_params.get('language', 'en')
        return translate_text(obj.full_description, language)

    class Meta:
        model = Service
        fields = ['id', 'slug', 'category', 'title', 'translated_short_description', 'translated_full_description',
                  'icon', 'image', 'meta_title', 'meta_description', 'created_at']


class CitySerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    locations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = City
        fields = ['id', 'name', 'province', 'services', 'locations', 'meta_title', 'meta_description', 'created_at']


class LocationSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()

    class Meta:
        model = Location
        fields = ['id', 'name', 'city', 'address', 'created_at']


class ContactSerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), required=False)
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), required=False)
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), required=False)

    class Meta:
        model = Contact
        fields = ['id', 'name', 'phone', 'email', 'address', 'description', 'city', 'service', 'location', 'created_at']

    def validate_name(self, value):
        if not value or len(value) > 70:
            raise serializers.ValidationError("Имя должно быть не длиннее 70 символов и не пустым")
        return value

    def validate_phone(self, value):
        import re
        pattern = r'^\+1\s*[\(\.]*\d{3}[\)\.\-]*\s*\d{3}[\.\-]*\s*\d{4}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Неверный формат телефона. Пример: +1 (123) 456-7890")
        digits = re.sub(r'\D', '', value)
        if len(digits) != 11 or not digits.startswith('1'):
            raise serializers.ValidationError("Номер должен содержать 10 цифр после +1")
        normalized = f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:11]}"
        return normalized

    def validate_email(self, value):
        if not value or '@' not in value:
            raise serializers.ValidationError("Неверный формат email")
        return value

    def validate_address(self, value):
        if not value:
            raise serializers.ValidationError("Адрес обязателен")
        return value

    def validate_description(self, value):
        if not value:
            raise serializers.ValidationError("Описание обязательно")
        return value


class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.SlugRelatedField(slug_field='slug', queryset=Brand.objects.all())
    pros = serializers.ListField(child=serializers.CharField(), read_only=True, source='pros.splitlines')
    cons = serializers.ListField(child=serializers.CharField(), read_only=True, source='cons.splitlines')


    class Meta:
        model = Product
        fields = ['id', 'brand', 'name', 'slug', 'description', 'pros', 'cons', 'created_at', 'updated_at']


class BlogPostSerializer(serializers.ModelSerializer):
    translated_title = serializers.SerializerMethodField()
    translated_content = serializers.SerializerMethodField()

    def get_translated_title(self, obj):
        language = self.context['request'].query_params.get('language', 'en')
        return translate_text(obj.title, language)

    def get_translated_content(self, obj):
        language = self.context['request'].query_params.get('language', 'en')
        return translate_text(obj.content, language)

    class Meta:
        model = BlogPost
        fields = ['id', 'slug', 'translated_title', 'translated_content', 'category', 'image', 'meta_title',
                  'meta_description', 'created_at']


class BrandSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    translated_name = serializers.SerializerMethodField(
        help_text="Translated brand name based on the requested language"
    )
    translated_description = serializers.SerializerMethodField(
        help_text="Translated brand description based on the requested language"
    )

    def get_translated_name(self, obj):
        language = self.context['request'].query_params.get('language', 'en')
        from integrations.google_translate import translate_text
        return translate_text(obj.name, language)

    def get_translated_description(self, obj):
        language = self.context['request'].query_params.get('language', 'en')
        from integrations.google_translate import translate_text
        return translate_text(obj.description, language)

    class Meta:
        model = Brand
        fields = ['id', 'slug', 'translated_name', 'translated_description', 'logo', 'meta_title', 'meta_description',
                  'created_at', 'products']


class AboutSerializer(serializers.ModelSerializer):
    translated_mission = serializers.SerializerMethodField()
    translated_experience = serializers.SerializerMethodField()

    def get_translated_mission(self, obj):
        language = self.context['request'].query_params.get('language', 'en')
        return translate_text(obj.mission, language)

    def get_translated_experience(self, obj):
        language = self.context['request'].query_params.get('language', 'en')
        return translate_text(obj.experience, language)

    class Meta:
        model = About
        fields = ['id', 'translated_mission', 'translated_experience', 'meta_title', 'meta_description', 'created_at']


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'position', 'photo', 'bio', 'created_at']


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ['id', 'image', 'description', 'created_at']


class CaseStudySerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()

    class Meta:
        model = CaseStudy
        fields = ['id', 'slug', 'title', 'description', 'image', 'city', 'meta_title', 'meta_description', 'created_at']


class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ['id', 'title', 'slug', 'description', 'requirements', 'salary', 'created_at', 'updated_at',
                  'is_active']


class VacancyApplicationSerializer(serializers.ModelSerializer):
    vacancy = serializers.SlugRelatedField(slug_field='slug', queryset=Vacancy.objects.all())

    class Meta:
        model = VacancyApplication
        fields = ['id', 'vacancy', 'name', 'email', 'phone', 'resume', 'message', 'created_at']



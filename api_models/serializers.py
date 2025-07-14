from rest_framework import serializers
from .models import City, Location, Service, Contact, Brand, BlogPost, About, CaseStudy, Product, BlogImage, \
    VacancyApplication, Vacancy, FAQ
from integrations.google_translate import translate_text


class ServiceSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    title = serializers.CharField(source='get_type_service_display')  # Corrected from get_title_display
    translated_full_description = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.get_category()

    def get_translated_full_description(self, obj):
        language = self.context['request'].query_params.get('language', 'en')
        return translate_text(obj.full_description if obj.full_description else '', language)

    class Meta:
        model = Service
        fields = ['id', 'slug', 'category', 'title', 'translated_full_description', 'icon', 'image', 'created_at']


class CitySerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    locations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = City
        fields = ['id', 'name', 'province', 'services', 'locations', 'created_at']


class LocationSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()

    class Meta:
        model = Location
        fields = ['id', 'name', 'city', 'address', 'created_at']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'phone', 'email', 'address', 'description', 'created_at', 'sent_to_crm', 'status']

    def validate_name(self, value):
        if not value or len(value) > 70:
            raise serializers.ValidationError("Name must not exceed 70 characters and must not be empty")
        return value

    def validate_phone(self, value):
        if value:
            import re
            pattern = r'^\+1\s*[\(\.]*\d{3}[\)\.\-]*\s*\d{3}[\.\-]*\s*\d{4}$'
            if not re.match(pattern, value):
                raise serializers.ValidationError("Invalid phone format. Example: +1 (123) 456-7890")
            digits = re.sub(r'\D', '', value)
            if len(digits) != 11 or not digits.startswith('1'):
                raise serializers.ValidationError("Phone number must contain 10 digits after +1")
            return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:11]}"
        return value

    def validate_email(self, value):
        if not value or '@' not in value:
            raise serializers.ValidationError("Invalid email format")
        return value

    def validate_address(self, value):
        if not value:
            raise serializers.ValidationError("Address is required")
        return value

    def validate_description(self, value):
        if value is None:
            return value
        return value


class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.SlugRelatedField(slug_field='slug', queryset=Brand.objects.all())
    pros = serializers.ListField(child=serializers.CharField(), read_only=True, source='pros.splitlines')
    cons = serializers.ListField(child=serializers.CharField(), read_only=True, source='cons.splitlines')

    class Meta:
        model = Product
        fields = ['id', 'brand', 'name', 'slug', 'description', 'created_at', 'updated_at']


class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = ['id', 'image', 'caption', 'created_at']


class BlogPostSerializer(serializers.ModelSerializer):
    images = BlogImageSerializer(many=True, required=False)  # Вложенное поле для нескольких изображений

    def get_translated_title(self, obj):
        language = self.context['request'].query_params.get('language', 'en')
        return translate_text(obj.title, language)

    def get_translated_content(self, obj):
        language = self.context['request'].query_params.get('language', 'en')
        return translate_text(obj.content, language)

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        blog_post = BlogPost.objects.create(**validated_data)
        for image_data in images_data:
            BlogImage.objects.create(blog_post=blog_post, **image_data)
        return blog_post

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.category = validated_data.get('category', instance.category)
        instance.video_on_youtube = validated_data.get('video_on_youtube', instance.video_on_youtube)
        instance.save()
        instance.images.all().delete()
        for image_data in images_data:
            BlogImage.objects.create(blog_post=instance, **image_data)
        return instance

    class Meta:
        model = BlogPost
        fields = ['title', 'id', 'slug','content', 'category', 'images', 'created_at']


class FAQSerializer(serializers.ModelSerializer):
    content_object_type = serializers.CharField(source='content_type.model', read_only=True)
    content_object_id = serializers.IntegerField(source='object_id', read_only=True)

    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'order', 'content_object_type', 'content_object_id']


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
        return translate_text(obj.name, language)

    def get_translated_description(self, obj):
        language = self.context['request'].query_params.get('language', 'en')
        return translate_text(obj.description, language)

    class Meta:
        model = Brand
        fields = ['id', 'slug', 'translated_name', 'translated_description', 'logo', 'created_at', 'products']


class BrandHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name', 'slug', 'logo']


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
        fields = ['id', 'translated_mission', 'translated_experience', 'created_at']


class CaseStudySerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()

    class Meta:
        model = CaseStudy
        fields = ['id', 'slug', 'title', 'description', 'image', 'city', 'created_at']


class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ['id', 'title', 'slug', 'conditions', 'location', 'created_at', 'updated_at', 'requirements',
                  'is_active']


class VacancyApplicationSerializer(serializers.ModelSerializer):
    vacancy = serializers.SlugRelatedField(slug_field='slug', queryset=Vacancy.objects.all())

    class Meta:
        model = VacancyApplication
        fields = ['id', 'vacancy', 'name', 'email', 'phone', 'resume', 'message', 'created_at']

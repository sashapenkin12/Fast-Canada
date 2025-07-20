from rest_framework import serializers
from .models import City, Location, Contact, Brand, BlogPost, About, CaseStudy, Product, BlogImage, \
    VacancyApplication, Vacancy, FAQ, Guarantee, Repair, Installation, CaseStudyImage, Promotion
from integrations.google_translate import translate_text


class CityHeaderSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_model_name', read_only=True)

    class Meta:
        model = City
        fields = ['name', 'slug', 'type']

    def get_model_name(self, obj):
        return obj._meta.model_name


class BaseServiceHeaderSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_model_name', read_only=True)

    class Meta:
        fields = ['name', 'slug', 'icon', 'cart_description']

    def get_model_name(self, obj):
        return obj._meta.model_name


class RepairCombinedServiceHeaderSerializer(BaseServiceHeaderSerializer):
    class Meta(BaseServiceHeaderSerializer.Meta):
        model = Repair


class InstallationCombinedServiceHeaderSerializer(BaseServiceHeaderSerializer):
    class Meta(BaseServiceHeaderSerializer.Meta):
        model = Installation


class ServiceHeaderSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_model_name', read_only=True)

    class Meta:
        fields = ['name', 'slug', 'icon', 'description', 'type']

    def get_model_name(self, obj):
        return obj._meta.model_name


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['id', 'title', 'description', 'date', 'created_at']


class RepairHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair
        fields = ['name', 'slug', 'icon']


class InstallationHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installation
        fields = ['name', 'slug', 'icon']


class GuaranteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guarantee
        fields = ['id', 'full_text', 'created_at']


class RepairSerializer(serializers.ModelSerializer):
    cities = serializers.SlugRelatedField(many=True, read_only=True, slug_field='slug')

    class Meta:
        model = Repair
        fields = ['id', 'name', 'slug', 'short_description', 'full_description', 'icon', 'image', 'created_at', 'cities']


class InstallationSerializer(serializers.ModelSerializer):
    cities = serializers.SlugRelatedField(many=True, read_only=True, slug_field='slug')

    class Meta:
        model = Installation
        fields = ['id', 'name', 'slug', 'short_description', 'full_description', 'icon', 'image', 'created_at', 'cities']


class LocationSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()

    class Meta:
        model = Location
        fields = ['id', 'name', 'city', 'latitude', 'longitude', 'created_at', 'place_id']


class CitySerializer(serializers.ModelSerializer):
    repair_services = RepairSerializer(many=True, read_only=True)
    installation_services = InstallationSerializer(many=True, read_only=True)
    locations = LocationSerializer(many=True, read_only=True)

    class Meta:
        model = City
        fields = ['id', 'name', 'province', 'repair_services', 'installation_services', 'locations', 'created_at',
                  'slug', 'latitude', 'longitude', 'place_id']


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

    class Meta:
        model = Product
        fields = ['id', 'brand', 'name', 'slug', 'description', 'created_at', 'updated_at', 'image']


class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = ['id', 'image', 'caption', 'created_at']


class BlogPostSerializer(serializers.ModelSerializer):
    images = BlogImageSerializer(many=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'content', 'category', 'video_on_youtube', 'created_at', 'images', 'text_for_cover', 'short_description']

    def validate_images(self, value):
        if not value:
            raise serializers.ValidationError("At least one image is required.")
        return value

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        blog_post = BlogPost.objects.create(**validated_data)
        for image_data in images_data:
            BlogImage.objects.create(blog_post=blog_post, **image_data)
        return blog_post

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if images_data is not None:
            instance.images.all().delete()
            for image_data in images_data:
                BlogImage.objects.create(blog_post=instance, **image_data)
        return instance


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


class CaseStudyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStudyImage
        fields = ['id', 'image', 'caption', 'created_at']


class CaseStudySerializer(serializers.ModelSerializer):
    images = CaseStudyImageSerializer(many=True, read_only=True)

    class Meta:
        model = CaseStudy
        fields = ['id', 'title', 'slug', 'short_description', 'description', 'city', 'created_at', 'video_on_youtube',
                  'images']

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


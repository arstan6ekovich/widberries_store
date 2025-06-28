from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import (
    UserProfile, Category, SubCategory, Product,
    ProductImage, Review, Basket, BasketItem
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number', 'status')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return UserProfile.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['product_image']


class ReviewSerializer(serializers.ModelSerializer):
    created_date = serializers.DateField(format='%d-%m-%Y')
    user = UserProfileSimpleSerializer()

    class Meta:
        model = Review
        fields = ['user', 'rating', 'comment', 'created_date']


class SubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'subcategory_name']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'category_image']


class CategoryDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'category_image']


class SubCategoryDetailSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = SubCategory
        fields = ['id', 'subcategory_name', 'products']

    def get_products(self, obj):
        products = obj.products.all()
        return ProductListSerializer(products, many=True).data


class ProductListSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True, read_only=True)
    get_avg_rating = serializers.SerializerMethodField()
    get_count_user = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'product_name', 'product_price', 'type_status',
                  'article_number', 'get_avg_rating', 'get_count_user', 'product_images')

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_user(self, obj):
        return obj.get_count_user()


class ProductDetailSerializer(serializers.ModelSerializer):
    create_date = serializers.DateField(format='%d-%m-%Y')
    sub_category = SubCategoryListSerializer()
    category = CategoryListSerializer(source='sub_category.category')
    product_images = ProductImageSerializer(many=True, read_only=True)
    all_reviews = ReviewSerializer(read_only=True, many=True, source='review_set')

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_price', 'type_status',
                  'article_number', 'product_description', 'product_video',
                  'create_date', 'sub_category', 'category',
                  'product_images', 'all_reviews']


class BasketItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, source='product')
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = BasketItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


class BasketSerializer(serializers.ModelSerializer):
    items = BasketItemSerializer(many=True, read_only=True, source='basketitem_set')
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ['id', 'user', 'items', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()

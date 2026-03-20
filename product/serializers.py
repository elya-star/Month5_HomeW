from rest_framework import serializers
from .models import Category, Product, Review
from rest_framework.exceptions import ValidationError

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(source='products.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'category_name']

class ReviewSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product', 'product_title', 'created_at']

class ProductWithReviewsSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'category_name', 'reviews', 'average_rating']

class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=1000)
    price = serializers.FloatField(min_value=0.0)
    category_id = serializers.IntegerField()
    rating = serializers.ListField(child=serializers.IntegerField())

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Category is not exist')
        return category_id
    
    def validate_ratings(self, rating):
        ratings_from_db = Review.objects.filter(id__in=rating)
        if len(rating) != len(ratings_from_db):
            raise ValidationError('rating is not exist')
        return rating
    

class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=500)
    rating = serializers.IntegerField(min_value=1, max_value=5, required=False)
    product_id = serializers.IntegerField()
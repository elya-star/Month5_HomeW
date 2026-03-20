from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Avg
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, ProductWithReviewsSerializer

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all().annotate(products_count=Count('products'))
    serializer_class = CategorySerializer
    
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


class ReviewListView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def create(self, request, *args, **kwargs):
        stars = request.data.get('stars')
        if stars and (int(stars) < 1 or int(stars) > 5):
            return Response(
                {'error': 'Stars must be between 1 and 5'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'
    
    def update(self, request, *args, **kwargs):
        stars = request.data.get('stars')
        if stars and (int(stars) < 1 or int(stars) > 5):
            return Response(
                {'error': 'Stars must be between 1 and 5'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)
    
class ProductsWithReviewsView(generics.ListAPIView):
    queryset = Product.objects.all().prefetch_related('reviews')
    serializer_class = ProductWithReviewsSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        for product in queryset:
            reviews = product.reviews.all()
            if reviews:
                avg_rating = sum(review.stars for review in reviews) / reviews.count()
                product.average_rating = round(avg_rating, 1)
            else:
                product.average_rating = 0
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = []
        for item, product in zip(serializer.data, queryset):
            item['average_rating'] = product.average_rating
            data.append(item)
        
        return Response(data, status=status.HTTP_200_OK)
from django.contrib import admin
from django.urls import path, include
from product import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/categories/', views.CategoryListView.as_view()),
    path('api/v1/categories/<int:id>/', views.CategoryDetailView.as_view()),
    path('api/v1/products/', views.ProductListView.as_view()),
    path('api/v1/products/<int:id>/', views.ProductDetailView.as_view()),
    path('api/v1/reviews/', views.ReviewListView.as_view()),
    path('api/v1/reviews/<int:id>/', views.ReviewDetailView.as_view()),    
    path('api/v1/products/reviews/', views.ProductsWithReviewsView.as_view()),
    path('api/v1/users/', include('users.urls')),

]
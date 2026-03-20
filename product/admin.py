from django.contrib import admin
from .models import Category, Product, Review


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = 'title price category'.split()
@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = 'name'.split()
@admin.register(Review)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display = 'text product'.split()
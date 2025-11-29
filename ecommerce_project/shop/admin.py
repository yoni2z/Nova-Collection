# shop/admin.py

from django.contrib import admin
from .models import Category, Product, Cart, Order, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Allows admin to add one extra image field initially

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock']
    inlines = [ProductImageInline]  # Add this line to manage images inline

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price', 'status', 'created_at']

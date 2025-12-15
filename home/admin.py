from django.contrib import admin
from .models import Slide,Occasion,Product

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ['order', 'title', 'is_active', 'created_at']
    list_editable = ['is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']

@admin.register(Occasion)
class OccasionAdmin(admin.ModelAdmin):
    list_display = ['order', 'name', 'slug', 'is_active', 'created_at']
    list_editable = ['is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sale_price', 'original_price', 'discount_percentage', 
                    'rating', 'is_bestseller', 'in_stock', 'is_active', 'order']
    list_editable = ['is_bestseller', 'is_active', 'order']
    list_filter = ['is_bestseller', 'is_active', 'fabric', 'color']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Images', {
            'fields': ('image', 'image_hover')
        }),
        ('Pricing', {
            'fields': ('original_price', 'sale_price')
        }),
        ('Details', {
            'fields': ('fabric', 'color', 'stock_quantity')
        }),
        ('Ratings', {
            'fields': ('rating', 'review_count')
        }),
        ('Status', {
            'fields': ('is_bestseller', 'is_active', 'order')
        }),
    )
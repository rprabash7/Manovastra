from django.contrib import admin
from .models import Slide, Occasion, Product, Testimonial


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
    # ✅ ADD is_wedding here (3 places)
    list_display = ['name', 'category', 'sale_price', 'original_price', 'discount_percentage', 
                    'rating', 'is_bestseller', 'is_ready_to_wear', 'is_wedding', 'in_stock', 'is_active', 'order']
    list_editable = ['is_bestseller', 'is_ready_to_wear', 'is_wedding', 'is_active', 'order']
    list_filter = ['category', 'is_bestseller', 'is_ready_to_wear', 'is_wedding', 'is_active', 'fabric', 'color']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'description', 'category')
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
            'fields': ('is_bestseller', 'is_ready_to_wear', 'is_wedding', 'is_active', 'order')  # ✅ ADD is_wedding
        }),
    )

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'rating', 'location', 'is_featured', 'is_active', 'order', 'created_at']
    list_editable = ['is_featured', 'is_active', 'order']
    list_filter = ['rating', 'is_featured', 'is_active']
    search_fields = ['customer_name', 'review_text', 'location']
    
    fieldsets = (
        ('Customer Info', {
            'fields': ('customer_name', 'customer_image', 'location')
        }),
        ('Review', {
            'fields': ('review_text', 'rating', 'purchase_product')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured', 'order')
        }),
    )
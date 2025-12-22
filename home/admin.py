from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Slide, Category, Product, Testimonial, Order


# Banner Slides Admin
@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ['order', 'title', 'image_preview', 'is_active', 'created_at']
    list_editable = ['is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['order']
    
    def image_preview(self, obj):
        if obj.image_desktop:
            return format_html(
                '<img src="{}" style="width: 100px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image_desktop.url
            )
        return "No Image"
    image_preview.short_description = "Preview"


# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image_preview', 'product_count', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Image"
    
    def product_count(self, obj):
        return obj.products.filter(is_active=True).count()
    product_count.short_description = "Products"


# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'image_preview',
        'name',
        'category',
        'original_price',
        'sale_price',
        'stock_quantity',
        'is_bestseller',
        'is_active',
        'created_at'
    ]
    list_editable = ['sale_price', 'stock_quantity', 'is_bestseller', 'is_active']
    list_filter = ['category', 'is_bestseller', 'is_ready_to_wear', 'is_wedding', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'fabric', 'color', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['-created_at']
    list_display_links = ['image_preview', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Pricing', {
            'fields': ('original_price', 'sale_price')
        }),
        ('Images', {
            'fields': ('image', 'image_hover')
        }),
        ('Product Details', {
            'fields': ('fabric', 'color', 'rating', 'review_count')
        }),
        ('Special Collections', {
            'fields': ('is_bestseller', 'is_ready_to_wear', 'is_wedding', 'is_featured')
        }),
        ('Stock & Display', {
            'fields': ('stock_quantity', 'is_active', 'display_order')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Image"

# Testimonials Admin
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'rating', 'location', 'is_featured', 'is_active', 'created_at']
    list_editable = ['is_featured', 'is_active']
    list_filter = ['rating', 'is_featured', 'is_active', 'created_at']
    search_fields = ['customer_name', 'location', 'review_text', 'purchase_product']
    ordering = ['-created_at']


# Orders Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_id_short', 
        'customer_name', 
        'customer_phone',
        'product_name',
        'quantity',
        'total_amount', 
        'status',
        'created_at'
    ]
    
    list_filter = ['status', 'created_at', 'product__category']
    search_fields = [
        'order_id', 
        'customer_name', 
        'customer_email', 
        'customer_phone',
        'razorpay_order_id',
        'razorpay_payment_id'
    ]
    
    readonly_fields = [
        'order_id', 
        'razorpay_order_id', 
        'razorpay_payment_id',
        'razorpay_signature',
        'created_at',
        'updated_at',
        'payment_date'
    ]
    
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'status', 'tracking_id', 'admin_notes')
        }),
        ('Payment Details', {
            'fields': (
                'razorpay_order_id',
                'razorpay_payment_id',
                'razorpay_signature',
                'total_amount',
                'payment_date'
            )
        }),
        ('Customer Information', {
            'fields': (
                'customer_name',
                'customer_email',
                'customer_phone'
            )
        }),
        ('Delivery Address', {
            'fields': ('address', 'city', 'state', 'pincode')
        }),
        ('Product Details', {
            'fields': ('product', 'quantity', 'product_price')
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
                'shipped_date',
                'delivered_date'
            ),
            'classes': ('collapse',)
        }),
    )
    
    def order_id_short(self, obj):
        return obj.order_id[:20] + '...' if len(obj.order_id) > 20 else obj.order_id
    order_id_short.short_description = "Order ID"
    
    def product_name(self, obj):
        return obj.product.name[:30] + '...' if len(obj.product.name) > 30 else obj.product.name
    product_name.short_description = "Product"
    
    # Bulk Actions
    actions = ['mark_confirmed', 'mark_processing', 'mark_shipped', 'mark_delivered']
    
    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} order(s) marked as confirmed.')
    mark_confirmed.short_description = "Mark selected as Confirmed"
    
    def mark_processing(self, request, queryset):
        updated = queryset.update(status='processing')
        self.message_user(request, f'{updated} order(s) marked as processing.')
    mark_processing.short_description = "Mark selected as Processing"
    
    def mark_shipped(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='shipped', shipped_date=timezone.now())
        self.message_user(request, f'{updated} order(s) marked as shipped.')
    mark_shipped.short_description = "Mark selected as Shipped"
    
    def mark_delivered(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='delivered', delivered_date=timezone.now())
        self.message_user(request, f'{updated} order(s) marked as delivered.')
    mark_delivered.short_description = "Mark selected as Delivered"


# Customize Admin Site
admin.site.site_header = "Manovastra Admin Panel"
admin.site.site_title = "Manovastra"
admin.site.index_title = "Dashboard"

admin.site.enable_nav_sidebar = True  # Django 3.1+ sidebar navigation
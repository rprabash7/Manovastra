from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils import timezone
from .models import Slide, Occasion, Product, Testimonial, Order


# ✅ Simple Slide Admin
@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ['order', 'title', 'image_preview', 'is_active', 'created_at']
    list_editable = ['is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['order']
    
    def image_preview(self, obj):
        if obj.image_desktop:
            return format_html('<img src="{}" style="width: 100px; height: 50px; object-fit: cover; border-radius: 4px;" />', obj.image_desktop.url)
        return "No Image"
    image_preview.short_description = "Preview"


# ✅ Occasion Admin
@admin.register(Occasion)
class OccasionAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image_preview', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Preview"


# ✅ Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'name', 'category', 'sale_price', 'stock_quantity', 'stock_status', 'is_bestseller', 'is_active', 'created_at']
    list_editable = ['sale_price', 'stock_quantity', 'is_bestseller', 'is_active']
    list_filter = ['category', 'is_bestseller', 'is_ready_to_wear', 'is_wedding', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'fabric', 'color']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'category')
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
        ('Display Settings', {
            'fields': ('is_bestseller', 'is_ready_to_wear', 'is_wedding', 'is_active', 'display_order')
        }),
        ('Inventory', {
            'fields': ('stock_quantity',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Image"
    
    def stock_status(self, obj):
        if obj.stock_quantity == 0:
            return mark_safe('<span style="color: red; font-weight: bold;">⚠️ Out of Stock</span>')
        elif obj.stock_quantity <= 5:
            return mark_safe('<span style="color: orange; font-weight: bold;">⚡ Low Stock</span>')
        return mark_safe('<span style="color: green; font-weight: bold;">✓ In Stock</span>')
    stock_status.short_description = "Stock Status"


# ✅ Testimonial Admin
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'rating_stars', 'location', 'is_featured', 'is_active', 'created_at']
    list_editable = ['is_featured', 'is_active']
    list_filter = ['rating', 'is_featured', 'is_active', 'created_at']
    search_fields = ['customer_name', 'location', 'review_text', 'purchase_product']
    ordering = ['-created_at']
    
    def rating_stars(self, obj):
        return '⭐' * obj.rating
    rating_stars.short_description = "Rating"


# ✅ ORDER ADMIN
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_id_display', 
        'customer_info', 
        'product_info', 
        'quantity',
        'total_amount_display', 
        'status_display', 
        'payment_status',
        'created_at'
    ]
    
    list_filter = ['status', 'created_at', 'payment_date', 'product__category']
    search_fields = [
        'order_id', 
        'customer_name', 
        'customer_email', 
        'customer_phone',
        'razorpay_order_id',
        'razorpay_payment_id',
        'tracking_id'
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
    
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('📋 Order Information', {
            'fields': ('order_id', 'status', 'tracking_id', 'admin_notes')
        }),
        ('💳 Payment Details', {
            'fields': (
                'razorpay_order_id',
                'razorpay_payment_id',
                'razorpay_signature',
                'total_amount',
                'payment_date'
            )
        }),
        ('👤 Customer Information', {
            'fields': (
                'customer_name',
                'customer_email',
                'customer_phone'
            )
        }),
        ('📍 Delivery Address', {
            'fields': ('address', 'city', 'state', 'pincode')
        }),
        ('📦 Product Details', {
            'fields': ('product', 'quantity', 'product_price')
        }),
        ('📅 Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
                'shipped_date',
                'delivered_date'
            ),
            'classes': ('collapse',)
        }),
    )
    
    def order_id_display(self, obj):
        return format_html('<strong style="color: #2196F3;">#{}</strong>', obj.order_id[:15])
    order_id_display.short_description = "Order ID"
    
    def customer_info(self, obj):
        return format_html(
            '<strong>{}</strong><br/>'
            '<small>📞 {}</small><br/>'
            '<small>✉️ {}</small>',
            obj.customer_name,
            obj.customer_phone,
            obj.customer_email
        )
    customer_info.short_description = "Customer"
    
    def product_info(self, obj):
        return format_html(
            '{}<br/><small style="color: #666;">{}</small>',
            obj.product.name[:40],
            obj.product.get_category_display()
        )
    product_info.short_description = "Product"
    
    def total_amount_display(self, obj):
        return format_html('<strong style="color: #4CAF50; font-size: 16px;">₹{}</strong>', obj.total_amount)
    total_amount_display.short_description = "Amount"
    
    def status_display(self, obj):
        status_map = {
            'pending': ('🟡', '#FFC107'),
            'confirmed': ('🟢', '#4CAF50'),
            'processing': ('📦', '#2196F3'),
            'shipped': ('🚚', '#FF9800'),
            'delivered': ('✅', '#8BC34A'),
            'cancelled': ('❌', '#F44336'),
            'refunded': ('💰', '#9E9E9E'),
        }
        
        emoji, color = status_map.get(obj.status, ('', '#000'))
        
        return mark_safe(
            f'<span style="background: {color}; color: white; padding: 5px 12px; '
            f'border-radius: 20px; font-weight: bold; font-size: 12px;">'
            f'{emoji} {obj.get_status_display()}</span>'
        )
    status_display.short_description = "Status"
    
    def payment_status(self, obj):
        if obj.razorpay_payment_id:
            return mark_safe('<span style="color: #4CAF50; font-weight: bold;">✓ Paid</span>')
        return mark_safe('<span style="color: #F44336; font-weight: bold;">✗ Unpaid</span>')
    payment_status.short_description = "Payment"
    
    actions = [
        'mark_as_confirmed',
        'mark_as_processing',
        'mark_as_shipped',
        'mark_as_delivered',
        'mark_as_cancelled'
    ]
    
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
        self.message_user(request, f"{queryset.count()} orders marked as confirmed.")
    mark_as_confirmed.short_description = "✅ Mark as Confirmed"
    
    def mark_as_processing(self, request, queryset):
        queryset.update(status='processing')
        self.message_user(request, f"{queryset.count()} orders marked as processing.")
    mark_as_processing.short_description = "📦 Mark as Processing"
    
    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped', shipped_date=timezone.now())
        self.message_user(request, f"{queryset.count()} orders marked as shipped.")
    mark_as_shipped.short_description = "🚚 Mark as Shipped"
    
    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered', delivered_date=timezone.now())
        self.message_user(request, f"{queryset.count()} orders marked as delivered.")
    mark_as_delivered.short_description = "✅ Mark as Delivered"
    
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, f"{queryset.count()} orders cancelled.")
    mark_as_cancelled.short_description = "❌ Cancel Orders"


# ✅ Customize Admin Site
admin.site.site_header = "Manovastra E-Commerce Administration"
admin.site.site_title = "Manovastra Admin"
admin.site.index_title = "Welcome to Manovastra Admin Dashboard"

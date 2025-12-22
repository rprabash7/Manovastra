from django.db import models
from django.utils.text import slugify


class Slide(models.Model):
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    image_desktop = models.ImageField(upload_to='slides/desktop')
    image_mobile = models.ImageField(upload_to='slides/mobile', blank=True)
    link_url = models.URLField(blank=True, help_text="Slide click redirect URL")
    order = models.IntegerField(default=0, help_text="Display order (0, 1, 2...)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Banner Slide"
        verbose_name_plural = "Banner Slides"
    
    def __str__(self):
        return f"Slide {self.order} - {self.title or 'No Title'}"


# ============================================
# ✅ NEW FRESH MODELS START HERE
# ============================================

class Category(models.Model):
    """Product Categories"""
    name = models.CharField(max_length=100, help_text="Ex: Sarees, Gowns, Kurtis")
    slug = models.SlugField(unique=True, help_text="URL-friendly (auto-generated)")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Products Model"""
    # Basic Info
    name = models.CharField(max_length=200, help_text="Product name")
    slug = models.SlugField(unique=True, blank=True, help_text="URL-friendly (auto-generated)")
    description = models.TextField(blank=True, help_text="Product description")
    
    # Category (ForeignKey to Category model)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='products',
        help_text="Select category"
    )
    
    # Pricing
    original_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="MRP")
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Selling price")
    
    # Images
    image = models.ImageField(upload_to='products/', blank=True, null=True, help_text="Main product image")
    image_hover = models.ImageField(upload_to='products/hover/', blank=True, null=True, help_text="Hover image (optional)")
    
    # Details
    fabric = models.CharField(max_length=100, blank=True, help_text="Ex: Silk, Cotton")
    color = models.CharField(max_length=50, blank=True, help_text="Ex: Red, Blue")
    
    # Ratings
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0, help_text="Out of 5")
    review_count = models.IntegerField(default=0, help_text="Number of reviews")
    
    # Special Flags
    is_bestseller = models.BooleanField(default=False, help_text="Show in Bestsellers")
    is_ready_to_wear = models.BooleanField(default=False, help_text="Ready to Wear collection")
    is_wedding = models.BooleanField(default=False, help_text="Wedding collection")
    is_featured = models.BooleanField(default=False, help_text="Featured on homepage")
    
    # Stock & Status
    stock_quantity = models.IntegerField(default=0, help_text="Available quantity")
    is_active = models.BooleanField(default=True, help_text="Visible on website")
    
    # Ordering
    display_order = models.IntegerField(default=0, help_text="Display priority")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return f'/products/{self.slug}/'
    
    @property
    def discount_percentage(self):
        """Calculate discount percentage"""
        if self.original_price > self.sale_price:
            return int(((self.original_price - self.sale_price) / self.original_price) * 100)
        return 0
    
    @property
    def savings(self):
        """Calculate savings amount"""
        return self.original_price - self.sale_price
    
    @property
    def in_stock(self):
        """Check if product is in stock"""
        return self.stock_quantity > 0


class Testimonial(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    review_text = models.TextField()
    rating = models.IntegerField(default=5, help_text="Rating out of 5")
    purchase_product = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Customer Testimonial"
        verbose_name_plural = "Customer Testimonials"
    
    def __str__(self):
        return f"{self.customer_name} - {self.rating}★"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', '🟡 Pending Payment'),
        ('confirmed', '🟢 Payment Confirmed'),
        ('processing', '📦 Processing'),
        ('shipped', '🚚 Shipped'),
        ('delivered', '✅ Delivered'),
        ('cancelled', '❌ Cancelled'),
        ('refunded', '💰 Refunded'),
    ]
    
    # Order Details
    order_id = models.CharField(max_length=100, unique=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    razorpay_signature = models.CharField(max_length=200, blank=True)
    
    # Customer Details
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    
    # Delivery Address
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    
    # Product Details - ✅ FIXED with related_name
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.IntegerField(default=1)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Order Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    tracking_id = models.CharField(max_length=100, blank=True, help_text="Courier tracking ID")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    shipped_date = models.DateTimeField(null=True, blank=True)
    delivered_date = models.DateTimeField(null=True, blank=True)
    
    # Admin Notes
    admin_notes = models.TextField(blank=True, help_text="Internal notes for admin")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Customer Order"
        verbose_name_plural = "Customer Orders"
    
    def __str__(self):
        return f"Order #{self.order_id} - {self.customer_name}"
    
    @property
    def status_color(self):
        colors = {
            'pending': '#FFC107',
            'confirmed': '#4CAF50',
            'processing': '#2196F3',
            'shipped': '#FF9800',
            'delivered': '#8BC34A',
            'cancelled': '#F44336',
            'refunded': '#9E9E9E',
        }
        return colors.get(self.status, '#000')

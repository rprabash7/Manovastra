from django.db import models

class Slide(models.Model):
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    image_desktop = models.ImageField(upload_to='slides/desktop/')
    image_mobile = models.ImageField(upload_to='slides/mobile/', blank=True)
    link_url = models.URLField(blank=True, help_text="Slide click చేసినప్పుడు redirect URL")
    order = models.IntegerField(default=0, help_text="Display order (0, 1, 2...)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Banner Slide'
        verbose_name_plural = 'Banner Slides'
    
    def __str__(self):
        return f"Slide {self.order} - {self.title or 'No Title'}"

class Occasion(models.Model):
    """Shop By Occasion categories"""
    name = models.CharField(max_length=100, help_text="Ex: Gifting, Daily Wear")
    slug = models.SlugField(unique=True, help_text="URL-friendly name")
    image = models.ImageField(upload_to='occasions/')
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Shop Occasion'
        verbose_name_plural = 'Shop Occasions'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/occasions/{self.slug}/'
    
class Product(models.Model):
    """Bestseller Products"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    
    # Images
    image = models.ImageField(upload_to='products/')
    image_hover = models.ImageField(upload_to='products/', blank=True, help_text="Hover effect image")
    
    # Pricing
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Details
    fabric = models.CharField(max_length=100, blank=True, help_text="Ex: Chiffon, Georgette")
    color = models.CharField(max_length=50, blank=True)
    
    # Ratings
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0, help_text="Out of 5.0")
    review_count = models.IntegerField(default=0)
    
    # Status
    is_bestseller = models.BooleanField(default=False, help_text="Show in Bestsellers section")
    is_active = models.BooleanField(default=True)
    stock_quantity = models.IntegerField(default=0)
    
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return f'/products/{self.slug}/'
    
    def discount_percentage(self):
        if self.original_price > 0:
            discount = ((self.original_price - self.sale_price) / self.original_price) * 100
            return round(discount)
        return 0
    
    def savings(self):
        return self.original_price - self.sale_price
    
    def in_stock(self):
        return self.stock_quantity > 0
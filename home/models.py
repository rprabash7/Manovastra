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

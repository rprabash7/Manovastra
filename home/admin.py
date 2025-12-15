from django.contrib import admin
from .models import Slide,Occasion

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
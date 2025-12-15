from django.shortcuts import render
from .models import Slide, Occasion, Product

def welcome(request):
    slides = Slide.objects.filter(is_active=True)[:5]
    occasions = Occasion.objects.filter(is_active=True)[:4]
    bestsellers = Product.objects.filter(is_bestseller=True, is_active=True)[:8]
    
    return render(request, 'base.html', {
        'slides': slides,
        'occasions': occasions,
        'bestsellers': bestsellers
    })

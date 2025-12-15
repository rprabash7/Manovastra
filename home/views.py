from django.shortcuts import render
from .models import Slide, Occasion

def welcome(request):
    slides = Slide.objects.filter(is_active=True)[:5]
    occasions = Occasion.objects.filter(is_active=True)[:4]  # Max 4
    return render(request, 'base.html', {
        'slides': slides,
        'occasions': occasions
    })

from django.shortcuts import render
from .models import Slide

def welcome(request):
    slides = Slide.objects.filter(is_active=True)[:5]  # Max 5 active slides
    return render(request, 'base.html', {'slides': slides})

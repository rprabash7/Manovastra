from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Slide, Occasion, Product, Testimonial


def welcome(request):
    """Homepage view"""
    slides = Slide.objects.filter(is_active=True)[:5]
    occasions = Occasion.objects.filter(is_active=True)[:4]
    bestsellers = Product.objects.filter(is_bestseller=True, is_active=True)[:8]
    ready_to_wear = Product.objects.filter(is_ready_to_wear=True, is_active=True)[:8]
    wedding_products = Product.objects.filter(is_wedding=True, is_active=True)[:8]
    testimonials = Testimonial.objects.filter(is_active=True, is_featured=True)[:8]
    
    return render(request, 'base.html', {
        'slides': slides,
        'occasions': occasions,
        'bestsellers': bestsellers,
        'ready_to_wear': ready_to_wear,
        'wedding_products': wedding_products,
        'testimonials': testimonials,
    })


def subscribe_newsletter(request):
    """Newsletter subscription handler"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        try:
            # Validate email format
            validate_email(email)
            
            # TODO: Save to database or send to email service
            # Example: Newsletter.objects.create(email=email)
            
            messages.success(request, 'Successfully subscribed to newsletter! 🎉')
        except ValidationError:
            messages.error(request, 'Please enter a valid email address.')
        except Exception as e:
            messages.error(request, 'Something went wrong. Please try again.')
        
        return redirect('welcome')
    
    # GET request redirect to homepage
    return redirect('welcome')

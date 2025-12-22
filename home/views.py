from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import razorpay
import json

from .models import Slide, Category, Product, Testimonial


# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def welcome(request):
    """Homepage view"""
    slides = Slide.objects.filter(is_active=True)[:5]
    occasions = Category.objects.filter(is_active=True)[:4]
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


def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    return render(request, 'product_detail.html', {
        'product': product,
    })


def category_products(request, category_slug):
    """Display products filtered by category"""
    
    # Try to get category by slug
    category = None
    products = Product.objects.filter(is_active=True)
    
    # Special collections
    if category_slug == 'bestsellers':
        products = products.filter(is_bestseller=True)
        category_name = 'Best Sellers'
    elif category_slug == 'ready-to-wear':
        products = products.filter(is_ready_to_wear=True)
        category_name = 'Ready to Wear'
    elif category_slug == 'wedding':
        products = products.filter(is_wedding=True)
        category_name = 'Wedding Collection'
    elif category_slug == 'latest':
        category_name = 'Latest Collection'
    else:
        # Get category by slug
        try:
            category = Category.objects.get(slug=category_slug, is_active=True)
            products = products.filter(category=category)
            category_name = category.name
        except Category.DoesNotExist:
            category_name = 'All Products'
    
    products = products.order_by('-created_at')
    
    return render(request, 'products_list.html', {
        'products': products,
        'category_name': category_name,
        'category_slug': category_slug,
        'category': category,
    })



def order_summary(request, slug):
    """Order summary page - Buy Now"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    return render(request, 'order_summary.html', {
        'product': product,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
    })


# ✅ FIXED - CREATE RAZORPAY ORDER
@csrf_exempt
def create_order(request):
    """Create Razorpay order"""
    if request.method == 'POST':
        try:
            # Parse JSON data
            data = json.loads(request.body.decode('utf-8'))
            amount = data.get('amount', 0)
            
            # Validate amount
            if not amount or float(amount) <= 0:
                return JsonResponse({'error': 'Invalid amount'}, status=400)
            
            # Convert to paise (Razorpay needs amount in smallest currency unit)
            amount_in_paise = int(float(amount) * 100)
            
            # Create Razorpay order
            order_data = {
                'amount': amount_in_paise,
                'currency': 'INR',
                'payment_capture': 1
            }
            
            razorpay_order = razorpay_client.order.create(data=order_data)
            
            # Store order details in session
            request.session['pending_order'] = {
                'order_data': data,
                'razorpay_order_id': razorpay_order['id']
            }
            
            return JsonResponse({
                'order_id': razorpay_order['id'],
                'amount': razorpay_order['amount'],
                'currency': razorpay_order['currency']
            })
            
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            print(f"Error creating order: {e}")
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


# ✅ FIXED - VERIFY PAYMENT
@csrf_exempt
def verify_payment(request):
    """Verify Razorpay payment"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            
            # Verify signature
            params_dict = {
                'razorpay_order_id': data.get('razorpay_order_id'),
                'razorpay_payment_id': data.get('razorpay_payment_id'),
                'razorpay_signature': data.get('razorpay_signature')
            }
            
            razorpay_client.utility.verify_payment_signature(params_dict)
            
            # Payment verified successfully
            order_id = data.get('razorpay_order_id')
            
            # Clear session
            if 'pending_order' in request.session:
                del request.session['pending_order']
            
            return JsonResponse({
                'success': True,
                'order_id': order_id
            })
            
        except razorpay.errors.SignatureVerificationError as e:
            print(f"Signature Verification Error: {e}")
            return JsonResponse({'success': False, 'error': 'Payment verification failed'}, status=400)
        except Exception as e:
            print(f"Error verifying payment: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def order_success(request):
    """Order success page"""
    order_id = request.GET.get('order_id', 'N/A')
    
    return render(request, 'order_success.html', {
        'order_id': order_id
    })


def subscribe_newsletter(request):
    """Newsletter subscription handler"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        try:
            validate_email(email)
            messages.success(request, 'Successfully subscribed to newsletter! 🎉')
        except ValidationError:
            messages.error(request, 'Please enter a valid email address.')
        except Exception as e:
            messages.error(request, 'Something went wrong. Please try again.')
        
        return redirect('welcome')
    
    return redirect('welcome')

# Update verify_payment function to save order

@csrf_exempt
def verify_payment(request):
    """Verify Razorpay payment"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            
            # Verify signature
            params_dict = {
                'razorpay_order_id': data.get('razorpay_order_id'),
                'razorpay_payment_id': data.get('razorpay_payment_id'),
                'razorpay_signature': data.get('razorpay_signature')
            }
            
            razorpay_client.utility.verify_payment_signature(params_dict)
            
            # ✅ SAVE ORDER TO DATABASE
            from .models import Order
            from django.utils import timezone
            
            product = Product.objects.get(slug=data.get('product_slug'))
            
            order = Order.objects.create(
                order_id=data.get('razorpay_order_id'),
                razorpay_order_id=data.get('razorpay_order_id'),
                razorpay_payment_id=data.get('razorpay_payment_id'),
                razorpay_signature=data.get('razorpay_signature'),
                
                customer_name=data.get('full_name'),
                customer_email=data.get('email'),
                customer_phone=data.get('phone'),
                
                address=data.get('address'),
                city=data.get('city'),
                state=data.get('state'),
                pincode=data.get('pincode'),
                
                product=product,
                quantity=int(data.get('quantity', 1)),
                product_price=product.sale_price,
                total_amount=data.get('amount'),
                
                status='confirmed',
                payment_date=timezone.now()
            )
            
            # Clear session
            if 'pending_order' in request.session:
                del request.session['pending_order']
            
            return JsonResponse({
                'success': True,
                'order_id': order.order_id
            })
            
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

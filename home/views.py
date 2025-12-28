from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from decimal import Decimal
import razorpay
import json

from .models import Slide, Category, Product, Testimonial, Cart, Order, Wishlist


# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def welcome(request):
    """Homepage view"""
    slides = Slide.objects.filter(is_active=True)[:5]
    occasions = Category.objects.filter(is_active=True)
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
    
    # Get color images
    color_images = product.color_images.all()
    available_colors = color_images.values_list('color', flat=True).distinct()
    
    return render(request, 'product_detail.html', {
        'product': product,
        'color_images': color_images,
        'available_colors': available_colors,
    })


def category_products(request, category_slug):
    """Display products filtered by category"""
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


@csrf_exempt
def create_order(request):
    """Create Razorpay order"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            amount = data.get('amount', 0)
            
            if not amount or float(amount) <= 0:
                return JsonResponse({'error': 'Invalid amount'}, status=400)
            
            amount_in_paise = int(float(amount) * 100)
            
            order_data = {
                'amount': amount_in_paise,
                'currency': 'INR',
                'payment_capture': 1
            }
            
            razorpay_order = razorpay_client.order.create(data=order_data)
            
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


@csrf_exempt
def verify_payment(request):
    """Verify Razorpay payment"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            
            params_dict = {
                'razorpay_order_id': data.get('razorpay_order_id'),
                'razorpay_payment_id': data.get('razorpay_payment_id'),
                'razorpay_signature': data.get('razorpay_signature')
            }
            
            razorpay_client.utility.verify_payment_signature(params_dict)
            
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
            
            if 'pending_order' in request.session:
                del request.session['pending_order']
            
            return JsonResponse({
                'success': True,
                'order_id': order.order_id
            })
            
        except razorpay.errors.SignatureVerificationError as e:
            print(f"Signature Verification Error: {e}")
            return JsonResponse({'success': False, 'error': 'Payment verification failed'}, status=400)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


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


def search_products(request):
    query = request.GET.get('q', '').strip()
    
    if not query or len(query) < 2:
        return JsonResponse({'products': [], 'count': 0})
    
    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(category__name__icontains=query) |
        Q(fabric__icontains=query)
    ).filter(is_active=True)[:10]
    
    results = []
    for product in products:
        results.append({
            'id': product.id,
            'name': product.name,
            'slug': product.slug,
            'price': str(product.sale_price),
            'original_price': str(product.original_price),
            'image': product.image.url if product.image else '',
            'url': product.get_absolute_url(),
            'category': product.category.name if product.category else '',
        })
    
    return JsonResponse({
        'products': results,
        'count': len(results)
    })


def get_session_key(request):
    """Get or create session key"""
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def add_to_wishlist(request, product_id):
    """Add product to wishlist"""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id, is_active=True)
        session_key = get_session_key(request)
        
        wishlist_item, created = Wishlist.objects.get_or_create(
            session_key=session_key,
            product=product
        )
        
        if created:
            message = f"{product.name} added to wishlist"
            status = 'added'
        else:
            message = "Already in wishlist"
            status = 'exists'
        
        wishlist_count = Wishlist.objects.filter(session_key=session_key).count()
        
        return JsonResponse({
            'success': True,
            'message': message,
            'status': status,
            'wishlist_count': wishlist_count
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def remove_from_wishlist(request, product_id):
    """Remove product from wishlist"""
    if request.method == 'POST':
        session_key = get_session_key(request)
        
        try:
            wishlist_item = Wishlist.objects.get(
                session_key=session_key,
                product_id=product_id
            )
            product_name = wishlist_item.product.name
            wishlist_item.delete()
            
            wishlist_count = Wishlist.objects.filter(session_key=session_key).count()
            
            return JsonResponse({
                'success': True,
                'message': f"{product_name} removed from wishlist",
                'wishlist_count': wishlist_count
            })
        except Wishlist.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Item not in wishlist'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def wishlist_page(request):
    """Display wishlist page"""
    session_key = get_session_key(request)
    wishlist_items = Wishlist.objects.filter(session_key=session_key).select_related('product')
    
    return render(request, 'wishlist.html', {
        'wishlist_items': wishlist_items,
        'wishlist_count': wishlist_items.count()
    })


def get_wishlist_count(request):
    """Get wishlist count for AJAX"""
    session_key = get_session_key(request)
    count = Wishlist.objects.filter(session_key=session_key).count()
    return JsonResponse({'count': count})


def add_to_cart(request, product_id):
    """Add product to cart"""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id, is_active=True)
        session_key = get_session_key(request)
        
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > product.stock_quantity:
            return JsonResponse({
                'success': False,
                'message': 'Not enough stock available'
            })
        
        cart_item, created = Cart.objects.get_or_create(
            session_key=session_key,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > product.stock_quantity:
                cart_item.quantity = product.stock_quantity
            cart_item.save()
            message = f"Updated {product.name} quantity"
        else:
            message = f"{product.name} added to cart"
        
        cart_count = Cart.objects.filter(session_key=session_key).count()
        
        return JsonResponse({
            'success': True,
            'message': message,
            'cart_count': cart_count
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def update_cart(request, product_id):
    """Update cart item quantity"""
    if request.method == 'POST':
        session_key = get_session_key(request)
        quantity = int(request.POST.get('quantity', 1))
        
        try:
            cart_item = Cart.objects.get(
                session_key=session_key,
                product_id=product_id
            )
            
            if quantity <= 0:
                cart_item.delete()
                message = "Item removed from cart"
            elif quantity > cart_item.product.stock_quantity:
                return JsonResponse({
                    'success': False,
                    'message': f'Only {cart_item.product.stock_quantity} units available'
                })
            else:
                cart_item.quantity = quantity
                cart_item.save()
                message = "Cart updated"
            
            cart_data = get_cart_data(session_key)
            
            return JsonResponse({
                'success': True,
                'message': message,
                'cart_data': cart_data
            })
        except Cart.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Item not in cart'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def remove_from_cart(request, product_id):
    """Remove product from cart"""
    if request.method == 'POST':
        session_key = get_session_key(request)
        
        try:
            cart_item = Cart.objects.get(
                session_key=session_key,
                product_id=product_id
            )
            product_name = cart_item.product.name
            cart_item.delete()
            
            cart_data = get_cart_data(session_key)
            
            return JsonResponse({
                'success': True,
                'message': f"{product_name} removed from cart",
                'cart_data': cart_data
            })
        except Cart.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Item not in cart'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def cart_page(request):
    """Display cart page"""
    session_key = get_session_key(request)
    cart_items = Cart.objects.filter(session_key=session_key).select_related('product')
    
    subtotal = sum(item.subtotal for item in cart_items)
    shipping = Decimal('0.00') if subtotal > 1000 else Decimal('1.00')
    total = subtotal + shipping
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'cart_count': cart_items.count(),
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total
    })


def get_cart_count(request):
    """Get cart count for AJAX"""
    session_key = get_session_key(request)
    count = Cart.objects.filter(session_key=session_key).count()
    return JsonResponse({'count': count})


def get_cart_data(session_key):
    """Helper function to get cart data"""
    cart_items = Cart.objects.filter(session_key=session_key).select_related('product')
    subtotal = sum(item.subtotal for item in cart_items)
    shipping = Decimal('0.00') if subtotal > 1000 else Decimal('50.00')
    total = subtotal + shipping
    
    return {
        'count': cart_items.count(),
        'subtotal': str(subtotal),
        'shipping': str(shipping),
        'total': str(total)
    }


def my_orders(request):
    """Display customer orders"""
    session_key = get_session_key(request)
    
    customer_email = request.session.get('customer_email', '')
    customer_phone = request.session.get('customer_phone', '')
    
    orders = Order.objects.none()
    
    if customer_email:
        orders = Order.objects.filter(customer_email=customer_email)
    elif customer_phone:
        orders = Order.objects.filter(customer_phone=customer_phone)
    
    return render(request, 'orders.html', {
        'orders': orders,
        'orders_count': orders.count()
    })


def order_detail(request, order_id):
    """Display order detail"""
    order = get_object_or_404(Order, order_id=order_id)
    
    return render(request, 'order_detail.html', {
        'order': order
    })


def track_order(request):
    """Track order by order ID"""
    order = None
    error = None
    
    if request.method == 'POST':
        order_id = request.POST.get('order_id', '').strip()
        email = request.POST.get('email', '').strip()
        
        try:
            order = Order.objects.get(order_id=order_id, customer_email=email)
        except Order.DoesNotExist:
            error = "Order not found. Please check your Order ID and Email."
    
    return render(request, 'track_order.html', {
        'order': order,
        'error': error
    })


def return_policy(request):
    """Return Policy Page"""
    return render(request, 'return_policy.html')

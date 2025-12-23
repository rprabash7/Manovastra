from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'), 
    path('category/<slug:category_slug>/', views.category_products, name='category_products'),
    path('order/<slug:slug>/', views.order_summary, name='order_summary'),
    
    # ✅ Payment URLs
    path('create-order/', views.create_order, name='create_order'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('order-success/', views.order_success, name='order_success'),

    path('search/', views.search_products, name='search_products'),

    # Wishlist URLs
    path('wishlist/', views.wishlist_page, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/count/', views.get_wishlist_count, name='wishlist_count'),

    # Cart URLs
    path('cart/', views.cart_page, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/count/', views.get_cart_count, name='cart_count'),

    # Order URLs
    path('orders/', views.my_orders, name='my_orders'),
    path('orders/<str:order_id>/', views.order_detail, name='order_detail'),
    path('track-order/', views.track_order, name='track_order'),

    # Policy URL
    path('return-policy/', views.return_policy, name='return_policy'),

]

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
]

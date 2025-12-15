from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
]

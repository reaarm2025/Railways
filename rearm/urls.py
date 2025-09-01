# core/urls.py
from django.contrib import admin
from django.urls import path
from rearm import views
from .views import book_demo_page

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('upload_media/', views.upload_media, name='upload_media'),
    path('book-demo/', book_demo_page, name='book_demo'),
    path('about/', views.about, name='about'),
    path('products/', views.product_list, name='product_list'),
    # path('products/<slug:slug>/', views.products_by_category, name='products_by_category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    # path('contact/', views.contact, name='contact'),
]

# urls.py


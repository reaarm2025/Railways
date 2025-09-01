from django.urls import path
from .views import (
    PostListView, 
    PostDetailView, 
    category_posts, 
    subscribe_newsletter,
    submit_contact,
    home
)

urlpatterns = [
    path('', home, name='post_list'),
    path('posts/', PostListView.as_view(), name='post_list_all'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:slug>/', category_posts, name='category_posts'),
    path('subscribe/', subscribe_newsletter, name='subscribe_newsletter'),
    path('contact/', submit_contact, name='submit_contact'),
]
import logging
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from django.conf import settings 
from cloudinary.models import CloudinaryField

logger = logging.getLogger(__name__)
User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)  

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = CKEditor5Field('Text', config_name='extends')
    if settings.DEBUG:
        featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    else:
        try:
            featured_image = CloudinaryField('featured_image', format='webp', folder='/about', null=True, blank=True)       
        except Exception as e:
            logger.error(f"Error uploading blog image: {e}")
    categories = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)  # ✅ FIXED
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email


# partnership


class PartnershipRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    position = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20)
    business_name = models.CharField(max_length=100)
    business_type = models.CharField(max_length=100)
    business_location = models.CharField(max_length=100, blank=True)
    interest = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Partnership request from {self.name}"


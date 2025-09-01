# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from datetime import datetime
import os

from .models import (
    Service, AboutSection, TeamMember, Leadership, Navbar,
    Product, ProductCategory
)
from blog.models import Post
from .forms import DemoBookingForm


def home(request):
    ceo_message = Leadership.objects.filter(is_ceo=True).first()  # CEO message
    about_content = AboutSection.objects.filter(is_active=True).first()
    featured_services = Service.objects.filter(is_featured=True)[:3]  # 3 featured services
    featured_products = Product.objects.filter(is_featured=True)[:3]  # 3 featured products
    blog_posts = Post.objects.filter(is_published=True).order_by('-created_at')[:4]  # latest 4 posts

    context = {
        'ceo': ceo_message,
        'blog_posts': blog_posts,
        'about_content': about_content,
        'page_name': 'home',
        'featured_services': featured_services,
        'featured_products': featured_products,
    }
    return render(request, "rearm/home.html", context)


def services(request):
    services = Service.objects.filter(is_featured=True)
    return render(request, 'rearm/services.html', {'services': services})


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    return render(request, 'rearm/service_detail.html', {'service': service})


@csrf_exempt
def upload_media(request):
    if request.FILES:
        file = request.FILES['file']
        # Create unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = os.path.splitext(file.name)[1]
        filename = f"uploads/{timestamp}{ext}"

        # Save file manually
        media_path = os.path.join('media', filename)
        os.makedirs(os.path.dirname(media_path), exist_ok=True)
        with open(media_path, 'wb+') as dest:
            for chunk in file.chunks():
                dest.write(chunk)

        return JsonResponse({
            'location': f"/media/{filename}"
        })
    return JsonResponse({'error': 'Invalid upload'}, status=400)


def book_demo_page(request):
    if request.method == 'POST':
        form = DemoBookingForm(request.POST)
        if form.is_valid():
            booking = form.save()

            # Your actual Calendly URL here
            calendly_url = "https://meet.brevo.com/reaarm"

            # Save Calendly link to booking
            booking.calendly_event_uri = calendly_url
            booking.save()

            return redirect(calendly_url)
    else:
        form = DemoBookingForm()

    return render(request, 'book_demo_page.html', {'form': form})


@require_GET
def about(request):
    try:
        about_content = AboutSection.objects.filter(is_active=True).latest('id')
        leadership = Leadership.objects.all().order_by('display_order')
    except AboutSection.DoesNotExist:
        about_content = None
        leadership = Leadership.objects.none()

    team_members = TeamMember.objects.filter(
        is_active=True,
        show_on_about=True
    ).order_by('order')

    context = {
        'leadership': leadership,
        'about_content': about_content,
        'team_members': team_members,
        'page_name': 'about',
        'meta_title': getattr(about_content, 'meta_title', 'About Us | Your Company'),
        'meta_description': getattr(about_content, 'meta_description', 'Learn about our company and team'),
        'canonical_url': request.build_absolute_uri(request.path)
    }
    return render(request, 'rearm/about.html', context)


def product_list(request):
    agricultural = Product.objects.filter(
        product_type='type1',
        is_active=True
    ).select_related('category')

    equipment = Product.objects.filter(
        product_type='type2',
        is_active=True
    ).select_related('category')

    context = {
        'agricultural_products': agricultural,
        'equipment_products': equipment,
    }
    return render(request, 'rearm/products/list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'rearm/products/detail.html', context)

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post, Category, NewsletterSubscriber
from .forms import NewsletterForm
from django.http import JsonResponse
from django.core.paginator import Paginator

def home(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    featured_posts = Post.objects.filter(is_published=True).order_by('-created_at')[:3]
    recent_posts = Post.objects.filter(is_published=True).order_by('-created_at')[3:6]
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = NewsletterForm()
    
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'featured_posts': featured_posts,
        'recent_posts': recent_posts,
        'categories': categories,
        'newsletter_form': form
    })

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        return Post.objects.filter(is_published=True).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.filter(is_published=True).order_by('-created_at')[:5]
        context['categories'] = Category.objects.all()
        context['newsletter_form'] = NewsletterForm()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.filter(is_published=True).exclude(
            id=self.object.id
        ).order_by('-created_at')[:5]
        context['categories'] = Category.objects.all()
        context['newsletter_form'] = NewsletterForm()
        
        return context

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(categories=category, is_published=True).order_by('-created_at')
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/post_list.html', {
        'posts': page_obj,
        'category': category,
        'recent_posts': Post.objects.filter(is_published=True).order_by('-created_at')[:5],
        'categories': Category.objects.all(),
        'newsletter_form': NewsletterForm()
    })

# newsletter

def subscribe_newsletter(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        email = request.POST.get('email')
        
        # Basic validation
        if not email or '@' not in email:
            return JsonResponse({
                'success': False,
                'errors': {'email': ['Please enter a valid email address']}
            }, status=400)
            
        try:
            # Create or get existing subscription
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=email,
                defaults={'email': email}
            )
            
            if not created:
                return JsonResponse({
                    'success': False,
                    'errors': {'email': ['This email is already subscribed']}
                }, status=400)
                
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'errors': {'general': ['An error occurred. Please try again later.']}
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'errors': {'general': ['Invalid request method']}
    }, status=400)

# partnership
from django.http import JsonResponse
from .models import PartnershipRequest

def submit_contact(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            # Create new partnership request
            PartnershipRequest.objects.create(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                position=request.POST.get('position', ''),
                phone=request.POST.get('phone'),
                business_name=request.POST.get('business_name'),
                business_type=request.POST.get('business_type'),
                business_location=request.POST.get('business_location', ''),
                interest=request.POST.get('interest'),
                message=request.POST.get('message', '')
            )
            return JsonResponse({'success': True, 'message': 'Thank you for your submission!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)
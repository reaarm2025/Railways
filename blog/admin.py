from django import forms
from django.contrib import admin
from .models import Post, Category, NewsletterSubscriber, PartnershipRequest
from django_ckeditor_5.widgets import CKEditor5Widget

class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'content': CKEditor5Widget(config_name='default'),
        }

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'author', 'created_at', 'is_published')
    list_filter = ('is_published', 'categories', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)

from django.contrib import admin
from .models import PartnershipRequest

@admin.register(PartnershipRequest)
class PartnershipRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'business_name', 'business_type', 'submitted_at', 'status_icon')
    list_filter = ('business_type', 'submitted_at')
    search_fields = ('name', 'email', 'business_name', 'phone')
    list_per_page = 20
    date_hierarchy = 'submitted_at'
    readonly_fields = ('submitted_at',)
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'position')
        }),
        ('Business Details', {
            'fields': ('business_name', 'business_type', 'business_location')
        }),
        ('Request Information', {
            'fields': ('interest', 'message', 'submitted_at')
        }),
    )
    
    def status_icon(self, obj):
        return '📩'  # You can customize this with different icons based on status
    status_icon.short_description = 'Status'
    
    def has_add_permission(self, request):
        return False  # Disable adding new requests directly from admin
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def get_readonly_fields(self, request, obj=None):
        # Make all fields readonly after creation
        if obj:  # Editing an existing object
            return [f.name for f in self.model._meta.fields]
        return self.readonly_fields
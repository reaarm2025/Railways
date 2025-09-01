

# Register your models here.
from django.db import models
from django.contrib import admin
from .models import Navbar
from django.utils.safestring import mark_safe
from .models import HeroSection # hero section imported
from django_ckeditor_5.fields import CKEditor5Field
from .models import Service
from django.urls import reverse
from django.utils.html import format_html
from django.core.exceptions import ValidationError

# navbar added to admin
@admin.register(Navbar)
class NavbarAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'logo_preview')
    readonly_fields = ('logo_preview',)



# hero section
@admin.register(HeroSection)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('page', 'title', 'primary_cta_preview', 'secondary_cta_preview')
    fieldsets = (
        ('Content', {
            'fields': ('page', 'title', 'subtitle', 'background_image')
        }),
        ('Call-to-Actions', {
            'fields': (
                ('primary_cta_text', 'primary_cta_link'),
                ('secondary_cta_text', 'secondary_cta_link')
            ),
            'description': '''
                <strong>Link formats:</strong><br>
                • URL name: "services"<br>
                • Path: "/services/"<br>
                • Full URL: "https://example.com"<br>
                <span style="color:red">Note: URL names must exist in urls.py</span>
            '''
        }),
    )
    
    def primary_cta_preview(self, obj):
        return self._format_cta_preview(obj.primary_cta_text, obj.primary_cta_link)
    primary_cta_preview.short_description = 'Primary CTA'
    
    def secondary_cta_preview(self, obj):
        return self._format_cta_preview(obj.secondary_cta_text, obj.secondary_cta_link)
    secondary_cta_preview.short_description = 'Secondary CTA'
    
    def _format_cta_preview(self, text, link):
        if not text:
            return format_html('<span style="color:gray">-</span>')
        
        try:
            if not link:
                return f"{text} (no link)"
                
            if '/' in link or '.' in link:
                return format_html(
                    '{} → <a href="{}" target="_blank" style="color:green">{}</a>',
                    text, link, link
                )
            else:
                return format_html(
                    '{} → <a href="{}" style="color:green">{}</a>',
                    text, reverse(link), link
                )
        except Exception as e:
            return format_html(
                '<span style="color:red">{} → {} (Error: {})</span>',
                text, link, str(e)
            )
        

# services
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Field()},
    }
    list_display = ('title', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}



# demo bookings
from django.contrib import admin
from .models import DemoBooking

@admin.register(DemoBooking)
class DemoBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
    search_fields = ('name', 'email')
    list_filter = ('submitted_at',)



# about us
from .models import AboutSection, TeamMember

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'phone_number', 'is_active')
    list_editable = ('is_active',)
    fieldsets = (
        ('Header', {
            'fields': ('title', 'subtitle', 'phone_number')
        }),
        ('Content', {
            'fields': ('content', 'main_image', 'secondary_image')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        })
    )
    
# team member
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'order', 'is_active', 'show_on_about')
    list_editable = ('order', 'is_active', 'show_on_about')
    list_filter = ('is_active', 'show_on_about')
    search_fields = ('name', 'position')



# footer
from .models import CompanyInfo, SocialMedia

class SocialMediaInline(admin.TabularInline):
    model = SocialMedia
    extra = 1

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    inlines = [SocialMediaInline]
    list_display = ('name', 'email')
    
    def has_add_permission(self, request):
        # Allow only one company info entry
        return not CompanyInfo.objects.exists()
    



from django.contrib import admin
from .models import Product, ProductCategory

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    
    def product_count(self, obj):
        return obj.product_set.count()
    product_count.short_description = 'Products'

class ProductAdmin(admin.ModelAdmin):
    # add 'price' to list_display should you need price in future
    list_display = ('name', 'category', 'product_type',  'is_featured', 'is_active')
    list_filter = ('category', 'product_type', 'is_featured', 'is_active')
    search_fields = ('name', 'description')
    # add 'price',  to list_editable should you need price in admin
    list_editable = ('is_featured', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category', 'product_type')
        }),
        ('Images', {
            'fields': ('image', 'image_360'),
        }),
        ('Details', {
            'fields': ('description', ), # add 'price' to fields if you need it
        }),
        ('Flags', {
            'fields': ('is_featured', 'is_active'),
            'classes': ('collapse',),
        }),
    )


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)


# ceo admin

from .models import Leadership

@admin.register(Leadership)
class LeadershipAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'is_ceo', 'display_order')
    list_editable = ('display_order', 'is_ceo')
    list_filter = ('is_ceo',)
    search_fields = ('name', 'title')
    fieldsets = (
        (None, {
            'fields': ('name', 'title', 'is_ceo', 'photo', 'display_order')
        }),
        ('Content', {
            'fields': ('home_excerpt', 'full_bio')
        }),
    )
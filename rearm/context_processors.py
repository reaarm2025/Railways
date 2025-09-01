# rearm/context_processors.py
from datetime import datetime
from .models import CompanyInfo, Navbar, HeroSection

def global_context(request):
    """Provides ALL global data to templates"""
    context = {}
    
    # Navbar data
    context['navbar'] = Navbar.objects.first()
    
    # Hero sections
    context['hero_sections'] = {
        hero.page: hero for hero in HeroSection.objects.all()
    } if HeroSection.objects.exists() else {}
    
    # Footer data
    context['company'] = CompanyInfo.objects.first()
    context['current_year'] = datetime.now().year
    
    return context
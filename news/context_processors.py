from .models import Category, News
from django.db.models import Count
from news.models import SiteConfiguration

def categories(request):
    """Context processor to add categories to all templates."""
    return {
        'categories': Category.objects.all()
    }

def popular_news(request):
    """Context processor to add popular news to all templates."""
    # Get popular news based on hit count
    popular = News.objects.filter(status='published').order_by('-hit_count_generic__hits')[:5]
    return {
        'popular_news': popular
    }

def site_configuration(request):
    """
    Adiciona as configurações do site ao contexto de todos os templates.
    """
    return {
        'site_config': SiteConfiguration.get_solo(),
    } 
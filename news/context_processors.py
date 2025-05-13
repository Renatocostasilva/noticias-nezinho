from .models import Category, News
from django.db.models import Count

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
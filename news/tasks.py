import feedparser
import time
import logging
from django.core.cache import cache

from celery import shared_task
from .models import RSSFeed

logger = logging.getLogger(__name__)

@shared_task(name='news.tasks.atualizar_feeds_rss')
def atualizar_feeds_rss():
    """Tarefa agendada para atualizar todos os feeds RSS ativos e armazenar em cache."""
    logger.info("Iniciando atualização automática de feeds RSS")
    
    active_feeds = RSSFeed.objects.filter(active=True).order_by('order')
    all_feed_entries = []
    
    for feed in active_feeds:
        try:
            logger.info(f"Atualizando feed: {feed.name}")
            feed_data = feedparser.parse(feed.url)
            
            if not feed_data.entries:
                logger.warning(f"Feed {feed.name} não contém entradas")
                continue
            
            entries = []
            for entry in feed_data.entries[:feed.max_items]:
                # Tentar extrair a imagem do feed
                image_url = None
                if 'media_content' in entry and entry.media_content:
                    for media in entry.media_content:
                        if 'url' in media:
                            image_url = media['url']
                            break
                
                # Tentar extrair de enclosures
                if not image_url and 'enclosures' in entry and entry.enclosures:
                    for enclosure in entry.enclosures:
                        if 'url' in enclosure and enclosure.type and enclosure.type.startswith('image'):
                            image_url = enclosure.url
                            break
                
                # Tente extrair links de imagens do conteúdo usando expressões regulares
                if not image_url and 'description' in entry:
                    import re
                    img_pattern = re.compile(r'<img[^>]+src="([^">]+)"')
                    match = img_pattern.search(entry.description)
                    if match:
                        image_url = match.group(1)
                
                # Formatar a data de publicação, se disponível
                pub_date = None
                if 'published_parsed' in entry and entry.published_parsed:
                    pub_date = time.strftime('%Y-%m-%d', entry.published_parsed)
                elif 'updated_parsed' in entry and entry.updated_parsed:
                    pub_date = time.strftime('%Y-%m-%d', entry.updated_parsed)
                
                # Preparar o sumário
                summary = ''
                if 'summary' in entry:
                    summary = entry.summary
                elif 'description' in entry:
                    summary = entry.description
                
                entry_data = {
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.get('published', ''),
                    'pub_date': pub_date,
                    'summary': summary,
                    'image_url': image_url,
                    'source': feed.name,
                    'source_url': feed.url,
                    'category': feed.category.name if feed.category else ''
                }
                entries.append(entry_data)
            
            if entries:
                feed_info = {
                    'id': feed.id,
                    'name': feed.name,
                    'logo': feed.logo.url if feed.logo else None,
                    'entries': entries,
                    'category': feed.category.name if feed.category else 'Geral'
                }
                all_feed_entries.append(feed_info)
                logger.info(f"Feed {feed.name} atualizado com {len(entries)} entradas")
            else:
                logger.warning(f"Nenhuma entrada processada para o feed {feed.name}")
                
        except Exception as e:
            logger.error(f"Erro ao processar feed {feed.name}: {str(e)}")
    
    # Armazenar resultados em cache
    if all_feed_entries:
        cache.set('rss_feeds_cache', all_feed_entries, 3600)  # Cache por 1 hora
        logger.info(f"Cache de feeds RSS atualizado com {len(all_feed_entries)} feeds")
    else:
        logger.warning("Nenhum feed RSS foi atualizado para armazenar em cache")
    
    return f"Atualizados {len(all_feed_entries)} feeds RSS" 
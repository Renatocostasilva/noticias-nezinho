#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noticias.settings')
django.setup()

from news.models import RSSFeed, Category

def create_sample_feeds():
    """Criar feeds RSS de exemplo."""
    
    # Lista de feeds populares
    feeds = [
        {
            'name': 'G1 - Últimas Notícias',
            'url': 'https://g1.globo.com/rss/g1/',
            'order': 1,
        },
        {
            'name': 'UOL Notícias',
            'url': 'https://rss.uol.com.br/feed/noticias.xml',
            'order': 2,
        },
        {
            'name': 'Estadão',
            'url': 'https://www.estadao.com.br/rss/ultimas.xml',
            'order': 3,
        },
        {
            'name': 'Folha de S.Paulo',
            'url': 'https://feeds.folha.uol.com.br/emcimadahora/rss091.xml',
            'order': 4,
        },
        {
            'name': 'BBC Brasil',
            'url': 'https://www.bbc.com/portuguese/topicos/brasil/index.xml',
            'order': 5,
        },
    ]
    
    # Verificar se já existem feeds
    if RSSFeed.objects.exists():
        print("Já existem feeds RSS cadastrados. Não serão criados novos.")
        return
    
    # Obter categorias
    categories = list(Category.objects.all())
    
    # Criar os feeds
    for i, feed_data in enumerate(feeds):
        # Atribuir categoria se existir
        if categories and i < len(categories):
            feed_data['category'] = categories[i]
        
        feed = RSSFeed(
            name=feed_data['name'],
            url=feed_data['url'],
            order=feed_data['order'],
            active=True,
            max_items=5
        )
        
        if 'category' in feed_data:
            feed.category = feed_data['category']
        
        feed.save()
        print(f"Feed '{feed.name}' criado com sucesso.")
    
    print(f"Total: {len(feeds)} feeds RSS criados.")

if __name__ == '__main__':
    create_sample_feeds() 
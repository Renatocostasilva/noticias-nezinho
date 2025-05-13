#!/usr/bin/env python
import os
import sys
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noticias.settings')
django.setup()

from django.urls import get_resolver
from django.urls.resolvers import URLPattern, URLResolver

def list_urls(resolver=None, prefix=''):
    """Listar todas as URLs disponíveis no projeto."""
    if resolver is None:
        resolver = get_resolver()
    
    for pattern in resolver.url_patterns:
        if isinstance(pattern, URLResolver):
            # É um grupo de URLs
            new_prefix = prefix + pattern.pattern.regex.pattern
            list_urls(pattern, new_prefix)
        elif isinstance(pattern, URLPattern):
            # É uma URL individual
            name = pattern.name or '(sem nome)'
            url = prefix + pattern.pattern.regex.pattern
            print(f"{url} - {name}")

if __name__ == '__main__':
    print("URLs disponíveis no projeto:")
    print("============================")
    list_urls() 
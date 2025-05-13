#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noticias.settings')
django.setup()

from django.urls import reverse, NoReverseMatch

def check_url(url_name, *args, **kwargs):
    """Verificar se uma URL pode ser resolvida."""
    try:
        url = reverse(url_name, args=args, kwargs=kwargs)
        print(f"✅ URL '{url_name}' resolvida para: {url}")
        return True
    except NoReverseMatch as e:
        print(f"❌ Erro ao resolver URL '{url_name}': {e}")
        return False

def main():
    """Verificar URLs importantes do projeto."""
    print("Verificando URLs do projeto...")
    print("==============================")
    
    # URLs da aplicação news
    check_url('news:home')
    check_url('news:news_admin')
    check_url('news:admin_dashboard')
    check_url('news:news_create')
    check_url('news:news_update', pk=1)
    check_url('news:news_delete', pk=1)
    
    # URLs da aplicação accounts
    check_url('accounts:login')
    check_url('accounts:logout')
    check_url('accounts:profile')
    
    # URLs do admin do Django
    check_url('admin:index')
    
    print("\nVerificação concluída!")

if __name__ == '__main__':
    main() 
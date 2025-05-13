#!/usr/bin/env python
"""
Script para verificar se o admin do Django está configurado corretamente.
"""
import os
import sys
import django

# Configura o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noticias.settings')
django.setup()

from django.contrib.auth.models import User
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

def check_admin_url():
    """Verifica se a URL do admin está configurada corretamente."""
    try:
        admin_url = reverse('admin:index')
        print(f"✓ URL do admin configurada corretamente: {admin_url}")
        return True
    except NoReverseMatch:
        print("✗ Erro: URL do admin não encontrada.")
        return False

def check_superuser():
    """Verifica se existe pelo menos um superusuário."""
    superusers = User.objects.filter(is_superuser=True)
    if superusers.exists():
        print(f"✓ Superusuário encontrado: {superusers.first().username}")
        return True
    else:
        print("✗ Erro: Nenhum superusuário encontrado.")
        return False

def main():
    """Função principal."""
    print("=== Verificando configuração do Admin do Django ===")
    
    admin_url_ok = check_admin_url()
    superuser_ok = check_superuser()
    
    if admin_url_ok and superuser_ok:
        print("\n✓ O Admin do Django está configurado corretamente!")
        print("Para acessar o painel de administração, use a URL: http://127.0.0.1:8000/admin/")
    else:
        print("\n✗ Existem problemas com a configuração do Admin do Django.")
        
        if not admin_url_ok:
            print("  - Verifique se 'django.contrib.admin' está em INSTALLED_APPS no arquivo settings.py")
            print("  - Verifique se a URL do admin está configurada corretamente em urls.py")
        
        if not superuser_ok:
            print("  - Crie um superusuário usando o comando: python manage.py createsuperuser")

if __name__ == "__main__":
    main() 
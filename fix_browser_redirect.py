#!/usr/bin/env python
import os
import sys
import django
import webbrowser
from pathlib import Path

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noticias.settings')
django.setup()

from django.urls import reverse

def open_url_in_browser(url_name, *args, **kwargs):
    """Abrir uma URL no navegador."""
    try:
        url = reverse(url_name, args=args, kwargs=kwargs)
        full_url = f"http://127.0.0.1:8000{url}"
        print(f"Abrindo URL: {full_url}")
        webbrowser.open(full_url)
        return True
    except Exception as e:
        print(f"Erro ao abrir URL '{url_name}': {e}")
        return False

def main():
    """Abrir URLs importantes no navegador."""
    print("Abrindo URLs importantes no navegador...")
    print("======================================")
    
    # Perguntar qual URL abrir
    print("\nEscolha uma URL para abrir:")
    print("1. Página inicial")
    print("2. Painel de administração de notícias")
    print("3. Criar nova notícia")
    print("4. Editar notícia (ID=1)")
    print("5. Admin do Django")
    print("6. URL personalizada")
    
    choice = input("\nDigite o número da opção (ou Enter para sair): ")
    
    if choice == "1":
        open_url_in_browser('news:home')
    elif choice == "2":
        open_url_in_browser('news:news_admin')
    elif choice == "3":
        open_url_in_browser('news:news_create')
    elif choice == "4":
        news_id = input("Digite o ID da notícia (padrão: 1): ") or "1"
        open_url_in_browser('news:news_update', pk=int(news_id))
    elif choice == "5":
        open_url_in_browser('admin:index')
    elif choice == "6":
        custom_url = input("Digite a URL personalizada (sem http://127.0.0.1:8000): ")
        if custom_url:
            full_url = f"http://127.0.0.1:8000{custom_url}"
            print(f"Abrindo URL: {full_url}")
            webbrowser.open(full_url)
    
    print("\nVerificação concluída!")

if __name__ == '__main__':
    main() 
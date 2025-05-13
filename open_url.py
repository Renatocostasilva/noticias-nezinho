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

def main():
    """Abrir a URL correta no navegador."""
    print("Abrindo a URL correta no navegador...")
    print("===================================")
    
    # Obter o ID da notícia
    news_id = input("Digite o ID da notícia que deseja editar: ")
    try:
        news_id = int(news_id)
    except ValueError:
        print("❌ ID inválido. Por favor, digite um número inteiro.")
        return False
    
    # Construir a URL
    try:
        url = reverse('news:news_update', kwargs={'pk': news_id})
        full_url = f"http://127.0.0.1:8000{url}"
        print(f"URL construída: {full_url}")
        
        # Abrir no navegador
        print(f"Abrindo URL no navegador: {full_url}")
        webbrowser.open(full_url)
        
        print("\nURL aberta com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao construir ou abrir a URL: {e}")
        return False

if __name__ == '__main__':
    main() 
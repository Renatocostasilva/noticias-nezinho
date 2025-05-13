#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noticias.settings')
django.setup()

from news.models import News
from news.forms import NewsForm

def main():
    """Verificar se o formulário está sendo renderizado corretamente."""
    print("Verificando o formulário...")
    print("==========================")
    
    # Obter o ID da notícia
    news_id = input("Digite o ID da notícia que deseja verificar: ")
    try:
        news_id = int(news_id)
    except ValueError:
        print("❌ ID inválido. Por favor, digite um número inteiro.")
        return False
    
    # Obter a notícia
    try:
        news = News.objects.get(pk=news_id)
        print(f"✅ Notícia encontrada: {news.title}")
    except News.DoesNotExist:
        print(f"❌ Notícia com ID {news_id} não encontrada.")
        return False
    
    # Criar o formulário
    form = NewsForm(instance=news)
    
    # Verificar os campos do formulário
    print("\nCampos do formulário:")
    for field_name in form.fields:
        print(f"- {field_name}")
    
    # Verificar se o campo 'slug' está presente
    if 'slug' in form.fields:
        print("\n✅ Campo 'slug' está presente no formulário.")
    else:
        print("\n❌ Campo 'slug' NÃO está presente no formulário.")
    
    # Verificar se o campo 'publish_date' está presente
    if 'publish_date' in form.fields:
        print("✅ Campo 'publish_date' está presente no formulário.")
    else:
        print("❌ Campo 'publish_date' NÃO está presente no formulário.")
    
    print("\nVerificação concluída!")
    return True

if __name__ == '__main__':
    main() 
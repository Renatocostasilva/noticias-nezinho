#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noticias.settings')
django.setup()

from django.db import connection
from django.db.utils import OperationalError
from news.models import News, Category, Comment, Newsletter

def check_table_exists(table_name):
    """Verificar se uma tabela existe no banco de dados."""
    with connection.cursor() as cursor:
        try:
            cursor.execute(f"SELECT 1 FROM {table_name} LIMIT 1")
            print(f"✅ Tabela '{table_name}' existe no banco de dados.")
            return True
        except OperationalError:
            print(f"❌ Tabela '{table_name}' NÃO existe no banco de dados.")
            return False

def check_model_count(model, name):
    """Verificar a quantidade de registros de um modelo."""
    try:
        count = model.objects.count()
        print(f"✅ Modelo '{name}' tem {count} registros.")
        return count
    except OperationalError as e:
        print(f"❌ Erro ao contar registros do modelo '{name}': {e}")
        return None

def main():
    """Verificar o banco de dados."""
    print("Verificando o banco de dados...")
    print("==============================")
    
    # Verificar se as tabelas existem
    check_table_exists('news_news')
    check_table_exists('news_category')
    check_table_exists('news_comment')
    check_table_exists('news_newsletter')
    
    print("\nVerificando a quantidade de registros...")
    # Verificar a quantidade de registros
    check_model_count(News, 'News')
    check_model_count(Category, 'Category')
    check_model_count(Comment, 'Comment')
    check_model_count(Newsletter, 'Newsletter')
    
    print("\nVerificação concluída!")

if __name__ == '__main__':
    main() 
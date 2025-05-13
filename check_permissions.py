#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noticias.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from news.models import News, Category, Comment, Newsletter

def check_user_permissions(username):
    """Verificar as permissões de um usuário."""
    try:
        user = User.objects.get(username=username)
        print(f"✅ Usuário '{username}' encontrado.")
        
        # Verificar se é superusuário
        if user.is_superuser:
            print(f"✅ Usuário '{username}' é superusuário.")
        else:
            print(f"❌ Usuário '{username}' NÃO é superusuário.")
        
        # Verificar se é staff
        if user.is_staff:
            print(f"✅ Usuário '{username}' é staff.")
        else:
            print(f"❌ Usuário '{username}' NÃO é staff.")
        
        # Verificar permissões
        permissions = user.get_all_permissions()
        print(f"Permissões do usuário '{username}':")
        for perm in sorted(permissions):
            print(f"  - {perm}")
        
        return user
    except User.DoesNotExist:
        print(f"❌ Usuário '{username}' NÃO encontrado.")
        return None

def check_model_permissions(model_name):
    """Verificar as permissões de um modelo."""
    try:
        content_type = ContentType.objects.get(app_label='news', model=model_name.lower())
        permissions = Permission.objects.filter(content_type=content_type)
        
        print(f"Permissões do modelo '{model_name}':")
        for perm in permissions:
            print(f"  - {perm.codename}: {perm.name}")
        
        return permissions
    except ContentType.DoesNotExist:
        print(f"❌ Modelo '{model_name}' NÃO encontrado.")
        return None

def main():
    """Verificar as permissões."""
    print("Verificando as permissões...")
    print("===========================")
    
    # Verificar usuários
    print("\nUsuários:")
    users = User.objects.all()
    for user in users:
        print(f"- {user.username} (staff: {user.is_staff}, superuser: {user.is_superuser})")
    
    # Verificar permissões de um usuário específico
    username = input("\nDigite o nome de usuário para verificar as permissões (ou Enter para pular): ")
    if username:
        print()
        check_user_permissions(username)
    
    # Verificar permissões dos modelos
    print("\nVerificando permissões dos modelos:")
    check_model_permissions('News')
    
    print("\nVerificação concluída!")

if __name__ == '__main__':
    main() 
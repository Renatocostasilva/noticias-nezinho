#!/usr/bin/env python
"""
Script para criar perfis para usuários existentes que ainda não têm um perfil.
"""
import os
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noticias.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile

def criar_perfis_faltantes():
    """Cria perfis para usuários que ainda não têm um."""
    usuarios_sem_perfil = 0
    perfis_criados = 0
    
    for usuario in User.objects.all():
        try:
            # Tenta acessar o perfil do usuário
            perfil = usuario.profile
            print(f"Usuário {usuario.username} já possui perfil.")
        except UserProfile.DoesNotExist:
            # Se o perfil não existir, cria um novo
            UserProfile.objects.create(user=usuario)
            perfis_criados += 1
            print(f"Perfil criado para o usuário {usuario.username}.")
        except Exception as e:
            # Se ocorrer outro erro, registra
            print(f"Erro ao verificar perfil do usuário {usuario.username}: {e}")
            usuarios_sem_perfil += 1
    
    print(f"\nResumo:")
    print(f"Total de usuários: {User.objects.count()}")
    print(f"Perfis criados: {perfis_criados}")
    print(f"Usuários com erro: {usuarios_sem_perfil}")

if __name__ == "__main__":
    print("Iniciando criação de perfis faltantes...")
    criar_perfis_faltantes()
    print("Processo concluído!") 
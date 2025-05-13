#!/usr/bin/env python
"""
Script para configurar o ambiente de desenvolvimento.
"""
import os
import subprocess
import sys
from disqus_fix import patch_disqus

def install_dependencies():
    """Instala as dependências do projeto."""
    print("Instalando dependências...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Dependências instaladas com sucesso!")

def apply_patch():
    """Aplica o patch para corrigir o problema com o pacote django-disqus."""
    print("Aplicando patch para o django-disqus...")
    patch_disqus()

def setup_django():
    """Configura o Django."""
    print("Configurando o Django...")
    
    # Cria as migrações
    subprocess.check_call([sys.executable, "manage.py", "makemigrations"])
    
    # Aplica as migrações
    subprocess.check_call([sys.executable, "manage.py", "migrate"])
    
    print("Django configurado com sucesso!")

def main():
    """Função principal."""
    install_dependencies()
    apply_patch()
    setup_django()
    
    print("\nConfigurações concluídas com sucesso!")
    print("\nAgora você pode executar o servidor Django com o comando:")
    print("python manage.py runserver")
    
    # Pergunta se o usuário deseja criar um superusuário
    create_superuser = input("\nDeseja criar um superusuário? (s/n): ")
    if create_superuser.lower() == 's':
        subprocess.check_call([sys.executable, "manage.py", "createsuperuser"])

if __name__ == "__main__":
    main() 
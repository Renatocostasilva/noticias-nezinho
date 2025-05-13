#!/usr/bin/env python
"""
Script para corrigir o problema do banco de dados.
Este script irá recriar as migrações e aplicá-las novamente.
"""
import os
import subprocess
import sys
import shutil

def main():
    """Função principal para corrigir o banco de dados."""
    print("Iniciando a correção do banco de dados...")
    
    # Verifica se o ambiente virtual existe
    if not os.path.exists('venv'):
        print("Criando ambiente virtual...")
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        print("Ambiente virtual criado com sucesso!")
    
    # Ativa o ambiente virtual
    if sys.platform == 'win32':
        python_path = os.path.join('venv', 'Scripts', 'python.exe')
    else:
        python_path = os.path.join('venv', 'bin', 'python')
    
    # Remove o banco de dados existente
    if os.path.exists('db.sqlite3'):
        print("Removendo banco de dados existente...")
        os.remove('db.sqlite3')
        print("Banco de dados removido com sucesso!")
    
    # Remove as migrações existentes
    for app in ['news', 'accounts']:
        migrations_dir = os.path.join(app, 'migrations')
        if os.path.exists(migrations_dir):
            print(f"Removendo migrações existentes do app '{app}'...")
            # Remove todos os arquivos de migração, exceto __init__.py
            for file in os.listdir(migrations_dir):
                if file != '__init__.py' and file.endswith('.py'):
                    os.remove(os.path.join(migrations_dir, file))
            print(f"Migrações do app '{app}' removidas com sucesso!")
    
    # Cria as migrações para cada app
    print("Criando migrações para o app 'news'...")
    subprocess.check_call([python_path, "manage.py", "makemigrations", "news"])
    
    print("Criando migrações para o app 'accounts'...")
    subprocess.check_call([python_path, "manage.py", "makemigrations", "accounts"])
    
    # Aplica as migrações
    print("Aplicando migrações...")
    subprocess.check_call([python_path, "manage.py", "migrate"])
    
    print("\nBanco de dados corrigido com sucesso!")
    print("Agora você pode executar o servidor Django com o comando:")
    print("python manage.py runserver")
    
    # Pergunta se o usuário deseja criar um superusuário
    create_superuser = input("\nDeseja criar um superusuário? (s/n): ")
    if create_superuser.lower() == 's':
        subprocess.check_call([python_path, "manage.py", "createsuperuser"])
    
    # Pergunta se o usuário deseja iniciar o servidor
    start_server = input("\nDeseja iniciar o servidor Django? (s/n): ")
    if start_server.lower() == 's':
        print("\nIniciando o servidor Django...")
        print("Acesse o site em: http://127.0.0.1:8000/")
        print("Para acessar o painel de administração: http://127.0.0.1:8000/admin/")
        print("Pressione Ctrl+C para encerrar o servidor.")
        subprocess.check_call([python_path, "manage.py", "runserver"])

if __name__ == "__main__":
    main() 
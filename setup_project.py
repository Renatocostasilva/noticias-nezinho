#!/usr/bin/env python
"""
Script para configurar o projeto completo:
1. Resetar o banco de dados
2. Criar migrações
3. Aplicar migrações
4. Criar um superusuário
5. Inicializar o banco de dados com dados de exemplo
6. Iniciar o servidor Django
"""
import os
import sys
import subprocess
import shutil
import getpass
import time

def run_command(command, shell=False):
    """Executa um comando no terminal e retorna o resultado."""
    try:
        if shell:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        stdout, stderr = process.communicate()
        return {
            'success': process.returncode == 0,
            'stdout': stdout.decode('utf-8'),
            'stderr': stderr.decode('utf-8'),
            'returncode': process.returncode
        }
    except Exception as e:
        return {
            'success': False,
            'stdout': '',
            'stderr': str(e),
            'returncode': -1
        }

def reset_database():
    """Remove o banco de dados e os arquivos de migração."""
    print("\n=== Resetando o banco de dados ===")
    
    # Remove o banco de dados
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')
        print("✓ Banco de dados removido.")
    else:
        print("✓ Banco de dados não encontrado. Nada para remover.")
    
    # Remove os arquivos de migração
    apps = ['news', 'accounts']
    for app in apps:
        migrations_dir = os.path.join(app, 'migrations')
        if os.path.exists(migrations_dir):
            for filename in os.listdir(migrations_dir):
                file_path = os.path.join(migrations_dir, filename)
                if filename != '__init__.py' and os.path.isfile(file_path):
                    os.remove(file_path)
            print(f"✓ Arquivos de migração de '{app}' removidos.")
    
    print("✓ Reset do banco de dados concluído.")

def create_migrations():
    """Cria novas migrações."""
    print("\n=== Criando novas migrações ===")
    
    result = run_command(['python', 'manage.py', 'makemigrations', 'news', 'accounts'])
    if result['success']:
        print("✓ Migrações criadas com sucesso.")
    else:
        print("✗ Erro ao criar migrações:")
        print(result['stderr'])
        sys.exit(1)

def apply_migrations():
    """Aplica as migrações."""
    print("\n=== Aplicando migrações ===")
    
    result = run_command(['python', 'manage.py', 'migrate'])
    if result['success']:
        print("✓ Migrações aplicadas com sucesso.")
    else:
        print("✗ Erro ao aplicar migrações:")
        print(result['stderr'])
        sys.exit(1)

def create_superuser():
    """Cria um superusuário."""
    print("\n=== Criando superusuário ===")
    
    create = input("Deseja criar um superusuário? (s/n): ").lower()
    if create != 's':
        print("✓ Criação de superusuário pulada.")
        return
    
    username = input("Username: ")
    email = input("Email: ")
    password = getpass.getpass("Senha: ")
    password_confirm = getpass.getpass("Confirme a senha: ")
    
    if password != password_confirm:
        print("✗ As senhas não coincidem. Tente novamente.")
        return create_superuser()
    
    # Cria o superusuário usando o comando createsuperuser
    command = f"echo \"from django.contrib.auth.models import User; User.objects.create_superuser('{username}', '{email}', '{password}')\" | python manage.py shell"
    result = run_command(command, shell=True)
    
    if result['success'] or "already exists" in result['stderr']:
        print(f"✓ Superusuário '{username}' criado com sucesso.")
    else:
        print("✗ Erro ao criar superusuário:")
        print(result['stderr'])
        retry = input("Deseja tentar novamente? (s/n): ").lower()
        if retry == 's':
            return create_superuser()

def initialize_data():
    """Inicializa o banco de dados com dados de exemplo."""
    print("\n=== Inicializando dados de exemplo ===")
    
    initialize = input("Deseja inicializar o banco de dados com dados de exemplo? (s/n): ").lower()
    if initialize != 's':
        print("✓ Inicialização de dados pulada.")
        return
    
    result = run_command(['python', 'init_data.py'])
    if result['success']:
        print("✓ Dados de exemplo inicializados com sucesso.")
    else:
        print("✗ Erro ao inicializar dados de exemplo:")
        print(result['stderr'])

def start_server():
    """Inicia o servidor Django."""
    print("\n=== Iniciando o servidor Django ===")
    
    start = input("Deseja iniciar o servidor Django? (s/n): ").lower()
    if start != 's':
        print("✓ Inicialização do servidor pulada.")
        return
    
    print("Iniciando o servidor Django em http://127.0.0.1:8000/")
    print("Pressione Ctrl+C para parar o servidor.")
    
    try:
        subprocess.run(['python', 'manage.py', 'runserver'])
    except KeyboardInterrupt:
        print("\nServidor parado.")

def main():
    """Função principal."""
    print("=== Configuração do Projeto Notícias ===")
    
    # Verifica se o arquivo manage.py existe
    if not os.path.exists('manage.py'):
        print("✗ Arquivo manage.py não encontrado. Certifique-se de estar no diretório raiz do projeto.")
        sys.exit(1)
    
    # Executa as etapas de configuração
    reset_database()
    create_migrations()
    apply_migrations()
    create_superuser()
    initialize_data()
    start_server()
    
    print("\n=== Configuração concluída! ===")
    print("O projeto está pronto para uso.")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python
"""
Script para iniciar o projeto Notícias.
"""
import os
import subprocess
import sys
import time

def main():
    """Função principal para iniciar o projeto."""
    print("Iniciando o projeto Notícias...")
    
    # Verifica se o ambiente virtual existe
    if not os.path.exists('venv'):
        print("Criando ambiente virtual...")
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        print("Ambiente virtual criado com sucesso!")
    
    # Ativa o ambiente virtual
    if sys.platform == 'win32':
        python_path = os.path.join('venv', 'Scripts', 'python.exe')
        pip_path = os.path.join('venv', 'Scripts', 'pip.exe')
    else:
        python_path = os.path.join('venv', 'bin', 'python')
        pip_path = os.path.join('venv', 'bin', 'pip')
    
    # Instala as dependências
    print("Instalando dependências...")
    subprocess.check_call([pip_path, "install", "--upgrade", "pip"])
    subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])
    print("Dependências instaladas com sucesso!")
    
    # Cria as migrações para cada app
    print("Criando migrações para o app 'news'...")
    subprocess.check_call([python_path, "manage.py", "makemigrations", "news"])
    
    print("Criando migrações para o app 'accounts'...")
    subprocess.check_call([python_path, "manage.py", "makemigrations", "accounts"])
    
    # Verifica se há outras migrações pendentes
    print("Verificando outras migrações pendentes...")
    subprocess.check_call([python_path, "manage.py", "makemigrations"])
    
    # Aplica as migrações
    print("Aplicando migrações...")
    subprocess.check_call([python_path, "manage.py", "migrate"])
    
    # Verifica se o banco de dados foi criado corretamente
    print("Verificando se o banco de dados foi criado corretamente...")
    try:
        # Tenta executar um comando SQL simples para verificar se as tabelas existem
        subprocess.check_call([
            python_path, "manage.py", "shell", "-c",
            "from news.models import News; print('Tabela news_news existe!')"
        ])
        print("Banco de dados configurado com sucesso!")
    except subprocess.CalledProcessError:
        print("Erro ao verificar o banco de dados. Tentando corrigir...")
        # Força a recriação das migrações
        subprocess.check_call([python_path, "manage.py", "makemigrations", "--empty", "news"])
        subprocess.check_call([python_path, "manage.py", "migrate", "--fake-initial"])
        subprocess.check_call([python_path, "manage.py", "migrate"])
    
    # Pergunta se o usuário deseja criar um superusuário
    create_superuser = input("Deseja criar um superusuário? (s/n): ")
    if create_superuser.lower() == 's':
        subprocess.check_call([python_path, "manage.py", "createsuperuser"])
    
    # Inicia o servidor
    print("\nIniciando o servidor Django...")
    print("Acesse o site em: http://127.0.0.1:8000/")
    print("Para acessar o painel de administração: http://127.0.0.1:8000/admin/")
    print("Pressione Ctrl+C para encerrar o servidor.")
    subprocess.check_call([python_path, "manage.py", "runserver"])

if __name__ == "__main__":
    main() 
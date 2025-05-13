#!/usr/bin/env python
"""
Script para resetar o banco de dados e as migrações.
Este script é mais simples e não depende do ambiente virtual.
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

def run_command(command, check=True):
    """Executar um comando no terminal."""
    print(f"Executando: {command}")
    result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"ERRO: {result.stderr}")
    return result.returncode == 0

def main():
    """Resetar o banco de dados e as migrações."""
    print("Resetando o banco de dados e as migrações...")
    print("==========================================")
    
    # Verificar se o arquivo db.sqlite3 existe
    db_file = Path('db.sqlite3')
    if db_file.exists():
        print(f"Removendo banco de dados: {db_file}")
        db_file.unlink()
        print("✅ Banco de dados removido.")
    else:
        print("Banco de dados não encontrado. Continuando...")
    
    # Remover arquivos de migração
    for app in ['news', 'accounts']:
        migrations_dir = Path(app) / 'migrations'
        if migrations_dir.exists():
            print(f"Processando diretório de migrações: {migrations_dir}")
            
            # Manter apenas o arquivo __init__.py
            for migration_file in migrations_dir.glob('*.py'):
                if migration_file.name != '__init__.py':
                    print(f"Removendo arquivo de migração: {migration_file}")
                    migration_file.unlink()
            
            # Remover diretório __pycache__ se existir
            pycache_dir = migrations_dir / '__pycache__'
            if pycache_dir.exists():
                print(f"Removendo diretório: {pycache_dir}")
                shutil.rmtree(pycache_dir)
            
            print(f"✅ Migrações de {app} removidas.")
    
    # Criar novas migrações
    print("\nCriando novas migrações...")
    if not run_command("python manage.py makemigrations news accounts"):
        print("❌ Erro ao criar migrações.")
        return False
    
    # Aplicar migrações
    print("\nAplicando migrações...")
    if not run_command("python manage.py migrate"):
        print("❌ Erro ao aplicar migrações.")
        return False
    
    # Perguntar se deseja criar um superusuário
    print("\nDeseja criar um superusuário? (s/n)")
    choice = input().lower()
    if choice == 's':
        print("\nCriando superusuário...")
        run_command("python manage.py createsuperuser", check=False)
    
    # Perguntar se deseja iniciar o servidor
    print("\nDeseja iniciar o servidor Django? (s/n)")
    choice = input().lower()
    if choice == 's':
        print("\nIniciando o servidor Django...")
        run_command("python manage.py runserver", check=False)
    
    print("\nProcesso concluído com sucesso!")
    return True

if __name__ == '__main__':
    main() 
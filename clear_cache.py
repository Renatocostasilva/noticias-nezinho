#!/usr/bin/env python
import os
import subprocess
import shutil
from pathlib import Path

print("Limpando cache do Django e reiniciando o servidor...")

# Diretório do projeto
BASE_DIR = Path(__file__).resolve().parent

# Limpar arquivos .pyc
print("Removendo arquivos .pyc...")
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".pyc"):
            os.remove(os.path.join(root, file))
            print(f"Removido: {os.path.join(root, file)}")
    
    # Remover diretórios __pycache__
    for dir in dirs:
        if dir == "__pycache__":
            shutil.rmtree(os.path.join(root, dir))
            print(f"Removido: {os.path.join(root, dir)}")

# Reiniciar o servidor
print("\nReiniciando o servidor Django...")
try:
    # Matar qualquer processo runserver existente
    subprocess.run(["pkill", "-f", "runserver"], check=False)
    print("Processos antigos do servidor encerrados.")
    
    # Iniciar o servidor novamente
    print("Iniciando o servidor Django...")
    subprocess.Popen(["python", "manage.py", "runserver"])
    print("\nServidor reiniciado com sucesso!")
    print("Acesse: http://127.0.0.1:8000/")
    print("\nDica: Limpe o cache do seu navegador ou use uma janela anônima para testar.")
except Exception as e:
    print(f"Erro ao reiniciar o servidor: {e}") 
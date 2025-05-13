#!/usr/bin/env python
import os
import sys
import django
import random
import string
from pathlib import Path

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noticias.settings')
django.setup()

from django.conf import settings

def generate_random_string(length=8):
    """Gerar uma string aleatória."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def update_static_url():
    """Atualizar a URL estática para forçar o navegador a recarregar os arquivos estáticos."""
    settings_file = Path(settings.BASE_DIR) / 'noticias' / 'settings.py'
    
    if not settings_file.exists():
        print(f"❌ Arquivo de configurações não encontrado: {settings_file}")
        return False
    
    # Ler o arquivo de configurações
    with open(settings_file, 'r') as f:
        content = f.read()
    
    # Verificar se já existe um parâmetro de versão na URL estática
    if "STATIC_URL = '/static/'" in content:
        # Adicionar um parâmetro de versão
        random_version = generate_random_string()
        new_content = content.replace(
            "STATIC_URL = '/static/'", 
            f"STATIC_URL = '/static/?v={random_version}/'"
        )
        
        # Salvar o arquivo de configurações
        with open(settings_file, 'w') as f:
            f.write(new_content)
        
        print(f"✅ URL estática atualizada com versão: {random_version}")
        return True
    else:
        print("❌ Não foi possível encontrar a configuração STATIC_URL no arquivo de configurações.")
        return False

def main():
    """Ajudar a limpar o cache do navegador."""
    print("Ajudando a limpar o cache do navegador...")
    print("=======================================")
    
    # Atualizar a URL estática
    if update_static_url():
        print("\nA URL estática foi atualizada. Agora você precisa:")
        print("1. Reiniciar o servidor Django")
        print("2. Limpar o cache do navegador ou usar uma janela anônima")
        print("\nPara reiniciar o servidor, execute:")
        print("   ./clear_cache.py")
    else:
        print("\nNão foi possível atualizar a URL estática.")
        print("Tente limpar o cache do navegador manualmente ou usar uma janela anônima.")

if __name__ == '__main__':
    main() 
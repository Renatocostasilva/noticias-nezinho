"""
Patch para corrigir o problema com o pacote django-disqus.
Este script deve ser executado antes de iniciar o servidor Django.
"""
import os
import sys
import importlib.util
from pathlib import Path

def find_disqus_init():
    """Encontra o arquivo __init__.py do pacote django-disqus."""
    for path in sys.path:
        disqus_init = Path(path) / 'disqus' / '__init__.py'
        if disqus_init.exists():
            return disqus_init
    return None

def patch_disqus():
    """Corrige o problema com o pacote django-disqus."""
    disqus_init = find_disqus_init()
    if not disqus_init:
        print("Não foi possível encontrar o pacote django-disqus.")
        return False
    
    with open(disqus_init, 'r') as f:
        content = f.read()
    
    # Substitui a importação problemática
    if 'from django.utils.six.moves.urllib.parse import urlencode' in content:
        content = content.replace(
            'from django.utils.six.moves.urllib.parse import urlencode',
            'from urllib.parse import urlencode'
        )
        
        with open(disqus_init, 'w') as f:
            f.write(content)
        
        print("Pacote django-disqus corrigido com sucesso!")
        return True
    else:
        print("O arquivo já foi corrigido ou não contém a importação problemática.")
        return False

if __name__ == "__main__":
    patch_disqus() 
#!/usr/bin/env python
import os
import sys
import django
import re
from pathlib import Path

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noticias.settings')
django.setup()

def find_javascript_in_templates():
    """Encontrar código JavaScript nos templates."""
    templates_dir = Path('templates')
    js_files = []
    
    for path in templates_dir.glob('**/*.html'):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Verificar se há tags <script>
            script_tags = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
            
            if script_tags:
                js_files.append((str(path), len(script_tags)))
                print(f"Encontrado {len(script_tags)} tag(s) <script> em {path}")
                
                # Verificar se há redirecionamentos
                for script in script_tags:
                    if 'window.location' in script or 'location.href' in script:
                        print(f"  ⚠️ Redirecionamento encontrado em {path}:")
                        for line in script.split('\n'):
                            if 'window.location' in line or 'location.href' in line:
                                print(f"    {line.strip()}")
    
    return js_files

def main():
    """Verificar o JavaScript."""
    print("Verificando o JavaScript...")
    print("==========================")
    
    # Encontrar código JavaScript nos templates
    js_files = find_javascript_in_templates()
    
    if not js_files:
        print("\nNenhum código JavaScript encontrado nos templates.")
    else:
        print(f"\nEncontrado código JavaScript em {len(js_files)} arquivo(s).")
    
    print("\nVerificação concluída!")

if __name__ == '__main__':
    main() 
# This file is intentionally left empty to mark the directory as a Python package. 

# Importar o celery quando o Django iniciar
from __future__ import absolute_import, unicode_literals

# Isso garante que o app Celery é carregado quando o Django inicia
from .celery import app as celery_app

__all__ = ('celery_app',) 
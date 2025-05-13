"""
WSGI config for noticias project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noticias.settings')

application = get_wsgi_application() 
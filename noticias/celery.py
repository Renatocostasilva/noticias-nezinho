import os
from celery import Celery

# Definir o módulo de configuração Django padrão.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noticias.settings')

app = Celery('noticias')

# Utilizar configurações do Django para o Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobrir tarefas automaticamente em todos os apps instalados
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}') 
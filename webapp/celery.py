import os
from datetime import timedelta

from celery import Celery


# Establecer las opciones de django para la aplicación de celery.
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')

# Crear la aplicación de Celery
app = Celery('webapp')

# Especificamos que las variables de configuración de Celery se encuentran
# en el fichero `settings.py` de Django.
# El parámetro namespace es para decir que las variables de configuración de
# Celery en el fichero settings empiezan por el prefijo *CELERY_*
app.config_from_object('django.conf:settings', namespace='CELERY')

# Este método auto-registra las tareas para el broker.
# Busca tareas dentro de todos los archivos `tasks.py` que haya en las apps
# y las envía a Redis automáticamente.
app.autodiscover_tasks()
app.conf.CELERYBEAT_SCHEDULE = {
    # Executes at midnight
    # 'example_1': {
    #     'task': 'apps.core.tasks.example_task',
    #     'schedule': timedelta(minutes=5),
    #     'kwargs': dict(sync_all=False)
    # },
    # 'example_2': {
    #     'task': 'apps.core.tasks.example_task',
    #     'schedule': crontab(minute=0, hour=5),
    #     'kwargs': dict(sync_all=True)
    # },
}
app.conf.task_track_started = True
app.conf.CELERY_TIMEZONE = 'America/Lima'

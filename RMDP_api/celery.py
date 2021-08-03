from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RMDP_api.settings')

app = Celery('RMDP_api')
# app = Celery(__name__, broker="amqp://sunlight:sunlight123@localhost:5672/celery", backend="redis://localhost")
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')

app.config_from_object('django.conf:settings')
# Load task modules from all registered Django app configs.
# app.autodiscover_tasks()
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.autodiscover_tasks()
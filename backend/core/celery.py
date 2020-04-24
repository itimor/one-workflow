# -*- coding: utf-8 -*-
# author: itimor

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
celery_app = Celery('core', result_backend='django-db')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
# Load task modules from all registered Django app configs.
celery_app.autodiscover_tasks()
celery_app.loader.override_backends['django-db'] = 'django_celery_results.backends.database:DatabaseBackend'
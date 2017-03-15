"""
WSGI config for python_entry_task project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import newrelic.agent

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "python_entry_task.settings")

newrelic.agent.initialize('newrelic.ini', 'producion')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

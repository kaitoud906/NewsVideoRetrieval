"""
WSGI config for videoretrieval project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from static_ranges import Ranges
from dj_static import Cling, MediaCling

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoretrieval.settings')

application = Ranges(Cling(MediaCling(get_wsgi_application())))

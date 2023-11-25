"""
WSGI config for collecti_stamp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
    os.environ.setdefault('MODE', 'production')
else:
    os.environ.setdefault('MODE', 'deployment')

application = get_wsgi_application()

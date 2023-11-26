"""
WSGI config for collecti_stamp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'collecti_stamp.settings'
if os.environ.get('OKTETO'):
    os.environ.setdefault('MODE', 'production')
else:
    os.environ.setdefault('MODE', 'deployment')

print('MODE: {}'.format(os.environ.get('MODE')))
application = get_wsgi_application()

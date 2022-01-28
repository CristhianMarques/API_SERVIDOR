"""
WSGI config for API_SERVIDOR project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""
import os
import sys
import site
from django.core.wsgi import get_wsgi_application

# add python site packages, you can use virtualenvs also
site.addsitedir("C:/Program Files/Python37/Lib/site-packages")

# Add the app's directory to the PYTHONPATH 
sys.path.append('C:/DEV/API_SERVIDOR') 
sys.path.append('C:/DEV/API_SERVIDOR/API_SERVIDOR')  

os.environ['DJANGO_SETTINGS_MODULE'] = 'API_SERVIDOR.settings' 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "API_SERVIDOR.settings")  
 
application = get_wsgi_application()
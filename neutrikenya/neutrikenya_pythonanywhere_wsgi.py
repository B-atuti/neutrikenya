"""
WSGI config for NeutriKenya project to use on PythonAnywhere.
"""

import os
import sys

# Replace YOUR_USERNAME with your PythonAnywhere username
USERNAME = 'YOUR_USERNAME'

# Add the project directory to the system path
path = f'/home/{USERNAME}/neutrikenya'
if path not in sys.path:
    sys.path.append(path)

# Set the environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'neutrikenya.settings_pythonanywhere'

# Import Django and start the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application() 
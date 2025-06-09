"""
Production settings for PythonAnywhere deployment
"""
import os
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Update to your PythonAnywhere username
PYTHONANYWHERE_USERNAME = 'your_pythonanywhere_username'

ALLOWED_HOSTS = [f'{PYTHONANYWHERE_USERNAME}.pythonanywhere.com', 'www.neutrikenya.com']

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

# Simplified static file serving with Whitenoise
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
] + MIDDLEWARE

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Database - SQLite is fine for small sites and PythonAnywhere supports it well
# If you want to use MySQL on PythonAnywhere, you would configure it here
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': PYTHONANYWHERE_USERNAME + '$neutrikenya',
#         'USER': PYTHONANYWHERE_USERNAME,
#         'PASSWORD': 'your_database_password',
#         'HOST': PYTHONANYWHERE_USERNAME + '.mysql.pythonanywhere-services.com',
#         'PORT': '3306',
#         'OPTIONS': {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#         },
#     }
# }

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django_error.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
} 
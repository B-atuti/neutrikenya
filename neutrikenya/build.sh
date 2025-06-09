#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Make migrations
python manage.py makemigrations

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Create a superuser if it doesn't exist
python manage.py shell << 'EOF'
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
EOF 
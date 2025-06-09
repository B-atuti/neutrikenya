# Deploying NeutriKenya to PythonAnywhere

This guide will help you deploy your NeutriKenya website to PythonAnywhere.

## Step 1: Sign up for PythonAnywhere

If you don't already have an account, sign up at [PythonAnywhere](https://www.pythonanywhere.com/). The free tier should be sufficient to start with.

## Step 2: Prepare Your Code

1. Upload your project to GitHub or GitLab
2. Make sure you have a `requirements.txt` file (already created)

## Step 3: Create a Web App on PythonAnywhere

1. Go to the PythonAnywhere dashboard
2. Click on the "Web" tab
3. Click "Add a new web app"
4. Choose "Manual configuration"
5. Select the latest Python version (3.10+)

## Step 4: Clone Your Repository

In the PythonAnywhere Bash console:

```bash
# Clone your repository
git clone https://github.com/yourusername/neutrikenya.git

# Navigate to your project directory
cd neutrikenya
```

## Step 5: Set Up Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the required packages
pip install -r requirements.txt
```

## Step 6: Configure Your Web App

1. Go to the "Web" tab
2. Configure your WSGI file by clicking on the WSGI configuration file link
3. Replace the content with:

```python
import os
import sys

# Add your project directory to the system path
path = '/home/YOUR_USERNAME/neutrikenya'
if path not in sys.path:
    sys.path.append(path)

# Set the environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'neutrikenya.settings_pythonanywhere'

# Import Django and start the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

4. Save the file

## Step 7: Configure Static Files

1. In the "Web" tab, scroll down to "Static files"
2. Add the following entries:
   - URL: `/static/` - Directory: `/home/YOUR_USERNAME/neutrikenya/static`
   - URL: `/media/` - Directory: `/home/YOUR_USERNAME/neutrikenya/media`

## Step 8: Update Settings

1. Open `neutrikenya/neutrikenya/settings_pythonanywhere.py`
2. Update `PYTHONANYWHERE_USERNAME` with your actual PythonAnywhere username
3. If you're using MySQL, uncomment and update the database settings

## Step 9: Collect Static Files & Migrate Database

In the PythonAnywhere Bash console:

```bash
cd neutrikenya
source venv/bin/activate

# Set the Django settings module
export DJANGO_SETTINGS_MODULE=neutrikenya.settings_pythonanywhere

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate
```

## Step 10: Create Superuser (Optional)

If you need admin access:

```bash
python manage.py createsuperuser
```

## Step 11: Reload Your Web App

1. Go back to the "Web" tab
2. Click the "Reload" button for your web app

## Step 12: Visit Your Site

Your site should now be available at `your_username.pythonanywhere.com`

## Updating Your Site

When you need to update your site:

1. Pull the latest changes in the PythonAnywhere Bash console:
```bash
cd neutrikenya
git pull
```

2. Update packages if necessary:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

3. Collect static files and migrate if needed:
```bash
export DJANGO_SETTINGS_MODULE=neutrikenya.settings_pythonanywhere
python manage.py collectstatic --noinput
python manage.py migrate
```

4. Reload your web app from the "Web" tab

## Troubleshooting

Check the error logs in the "Web" tab if you encounter any issues. The logs section is at the bottom of the page and includes:
- Error log
- Server log
- Access log 
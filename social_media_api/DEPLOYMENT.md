🚀 Deployment of Django REST API (Production)
Project

social_media_api
Repository: Alx_DjangoLearnLab

1. Preparing the Project for Deployment
Production Settings

The Django project was configured for production by updating settings.py with the following changes:

DEBUG set to False

ALLOWED_HOSTS configured to allow the production domain

SQLite database used for production demo

Static files configured using STATIC_ROOT

Security headers enabled:

SECURE_BROWSER_XSS_FILTER = True

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"

Authentication

Token-based authentication enabled using Django REST Framework.

Custom user model (CustomUser) configured.

2. Hosting Service Selection
Hosting Platform

PythonAnywhere

PythonAnywhere was selected because:

It supports Django applications out of the box

Provides WSGI configuration

Free tier is suitable for demonstration projects

Public URL available for testing and portfolio use

3. Web Server and WSGI Setup

Django application served using PythonAnywhere’s WSGI server

Gunicorn installed as the WSGI HTTP server

WSGI configuration points to:

social_media_api.wsgi

4. Static Files and Database Management
Static Files

Static files configured using Django’s collectstatic

STATIC_ROOT defined as:

BASE_DIR / "staticfiles"


Static files mapped in PythonAnywhere Web dashboard:

URL: /static/

Directory: /home/maile/Alx_DjangoLearnLab/social_media_api/staticfiles

Media Files

Media files configured using:

MEDIA_URL

MEDIA_ROOT

Database

SQLite database used for production demo

Migrations applied using:

python manage.py migrate

5. Deployment Process
Steps Followed

Code pushed to GitHub repository

Project cloned on PythonAnywhere

Virtual environment created and activated

Dependencies installed using requirements.txt

Database migrations applied

Static files collected

Web app reloaded on PythonAnywhere

Environment Configuration

Virtual environment used to isolate dependencies

Production dependencies listed in requirements.txt

6. Monitoring and Maintenance
Monitoring

PythonAnywhere logs used for:

Error tracking

Runtime issues

Application health monitoring

Maintenance Plan

Regular dependency updates

Database backups when needed

Periodic security review

Token rotation if compromised

7. Final Testing

The following tests were performed on the live application:

User registration and login

Token authentication

Creating posts and comments

Liking and unliking posts

Receiving notifications

Accessing protected endpoints

Admin interface access

All features function as expected in the production environment.

8. Live Application URL

🌍 Live URL:

https://maile.pythonanywhere.com

9. Deployment Artifacts
Included in Repository

requirements.txt

Updated settings.py

WSGI configuration

Migration files

.gitignore

Deployment documentation (DEPLOYMENT.md)

✅ Conclusion

The Django REST API was successfully deployed to a production environment using PythonAnywhere.
The application is publicly accessible, secure, and fully functional, making it suitable for real-world testing and portfolio presentation.
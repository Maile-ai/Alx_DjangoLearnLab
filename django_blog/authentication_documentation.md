📘 Django Blog — User Authentication System Documentation
Overview

This document explains the complete authentication system implemented for the Django Blog application.
The system provides:

User registration

Login

Logout

Profile management

Form validation

Flash messages (success/error/info)

Secure, Django-compliant authentication flow

The implementation follows Django best practices and the ALX project requirements.

🔧 1. Features Implemented
✔ User Registration

Users can create an account by providing:

username

email

password

Validation includes:

password strength

password match

unique email

CSRF protection

After successful registration:

user is automatically logged in

redirected to /profile/

✔ User Login

Users enter:

username

password

On success:

redirected to /profile/

On failure:

error message displayed (invalid credentials)

✔ User Logout

Logging out:

destroys session

displays logout confirmation page

offers link to login again

✔ Profile Management

Authenticated users can:

View profile info

Edit username

Edit email

Profile updates:

validated

saved securely

success/error messages displayed

Access to /profile/ is restricted using:

@login_required

🗂 2. Project File Structure for Authentication
django_blog/
│
├── blog/
│   ├── views.py            # Register, login, logout, profile views
│   ├── models.py           # Profile model + signals
│   ├── forms.py            # CustomUserCreationForm, UserUpdateForm
│   ├── urls.py             # Authentication URL routes
│   └── templates/blog/
│       ├── base.html
│       ├── register.html
│       ├── login.html
│       ├── logout.html
│       └── profile.html
│
├── django_blog/
│   ├── settings.py         # Redirects, media setup, templates
│   └── urls.py             # Routing to the blog views

🛠 3. How the Authentication Works (Flow Explanation)
Registration Flow

User visits /register/

Fills form → CustomUserCreationForm

If valid:

User object created

login(request, user) logs them in

Redirect to /profile/

Displays success message

Login Flow

User visits /login/

Enters credentials → AuthenticationForm

If valid:

User authenticated & logged in

Redirect to /profile/

If not valid:

Error message shown

Logout Flow

User visits /logout/

Django session ends

Logout page rendered

Profile Flow

Only logged-in users can access /profile/

Shows editable form with current user info

On save → fields updated

Success message displayed

⚙ 4. Settings Required
In settings.py:
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "profile"
LOGOUT_REDIRECT_URL = "login"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

Context processors must include:
'django.template.context_processors.request',
'django.contrib.auth.context_processors.auth',
'django.contrib.messages.context_processors.messages',

🔗 5. URL Routes

In blog/urls.py:

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
]

🎨 6. Templates Overview
✔ base.html

Contains nav bar with Login/Register or Profile/Logout based on user.is_authenticated

Renders Django message alerts

Wraps all pages with a consistent layout

✔ register.html

Form for new user registration.

✔ login.html

Form for user login.

✔ logout.html

Simple confirmation page.

✔ profile.html

Form for editing username & email.

🧪 7. Manual Testing Instructions
✔ Registration Test

Go to /register/

Create a user

Should redirect to /profile/

Should be logged in

✔ Login Test

Go to /login/

Enter bad credentials → error message

Enter correct credentials → redirects to /profile/

✔ Logout Test

Go to /logout/

Should log out and display logout page

✔ Profile Update Test

While logged in → visit /profile/

Change username/email → save

Should update and show success message

✔ Access Control Test

Try /profile/ while logged OUT

Should redirect to /login/?next=/profile/

🧪 8. Automated Tests (Optional, but recommended)

Example included in blog/tests.py:

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthFlowTests(TestCase):
    def test_register_login_logout_profile(self):
        # Register
        resp = self.client.post(reverse("register"), {
            "username": "tester",
            "email": "test@example.com",
            "password1": "StrongPass!23",
            "password2": "StrongPass!23",
        })
        self.assertEqual(resp.status_code, 302)  # Redirect

        # Login
        resp = self.client.post(reverse("login"), {
            "username": "tester",
            "password": "StrongPass!23",
        })
        self.assertEqual(resp.status_code, 302)

        # Profile access
        self.client.login(username="tester", password="StrongPass!23")
        resp = self.client.get(reverse("profile"))
        self.assertEqual(resp.status_code, 200)


Run:

python manage.py test blog

🔒 9. Security Considerations

All forms include CSRF tokens

Passwords hashed using Django’s secure hashing

Profile page protected by @login_required

No sensitive data stored in plain text

Redirects properly validated

🎯 10. Conclusion

This authentication system provides a secure and clean login experience for the Django Blog project.
It meets all the ALX project requirements, including:

✔ registration
✔ login
✔ logout
✔ profile management
✔ template setup
✔ URL routing
✔ documentation
✔ testing
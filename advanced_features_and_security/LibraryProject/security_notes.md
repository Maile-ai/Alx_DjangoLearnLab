Django Security Best Practices — Implementation Summary

Project: LibraryProject
Author: Mokete Maile
Purpose: This document summarizes all security measures implemented in the Django project as part of the “Implementing Security Best Practices in Django” task.

Step 1: Secure Settings Configuration

DEBUG

DEBUG = False
Disabled in production to prevent exposure of sensitive debug information.

Allowed Hosts

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
Restricts valid hostnames to prevent host header attacks.

Browser Security Headers

SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True


These settings provide additional browser-level protection against:

Cross-Site Scripting (XSS)

Clickjacking

MIME-type sniffing

Secure Cookies

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


Ensures that cookies are only transmitted via HTTPS connections.

Step 2: Cross-Site Request Forgery (CSRF) Protection

Verified that all form templates include {% csrf_token %}.

Confirmed that django.middleware.csrf.CsrfViewMiddleware is active.

Manually tested forms to confirm that requests without a valid CSRF token are rejected with a 403 error.

Step 3: SQL Injection and Input Validation

Safe ORM Usage

All database queries use Django’s ORM methods (.get(), .filter(), .create(), .update(), .delete()).

No raw SQL statements are used.

Input Validation
A Django ModelForm (BookForm) was implemented to handle user input safely.

Example:

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long.")
        return title


This ensures that all user input is validated, sanitized, and escaped automatically before being saved.

Step 4: Content Security Policy (CSP)

Installed: django-csp middleware.

Middleware Added

'csp.middleware.CSPMiddleware',


CSP Settings

CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", 'https://fonts.googleapis.com',)
CSP_SCRIPT_SRC = ("'self'",)
CSP_IMG_SRC = ("'self'", 'data:')


Purpose

Restricts loading of external resources (scripts, styles, and images) to trusted sources.

Protects against XSS and data injection attacks.

Verified in browser developer tools under “Response Headers”.

Step 5: Documentation and Testing

Documentation

Comments added in settings.py and this document explaining each security setting.

Each measure includes a rationale for its inclusion.

Manual Testing

Security Area	Test Description	Expected Result
CSRF	Removed {% csrf_token %} and submitted form	403 Forbidden
XSS	Entered <script>alert('XSS')</script> in input	Displayed as plain text
SQL Injection	Entered '; DROP TABLE bookshelf_book;-- in input	Ignored safely
CSP	Added inline <script> in template	Blocked by browser
Summary

The following security measures have been successfully implemented:

Disabled DEBUG mode for production.

Restricted allowed hosts to trusted domains.

Added browser-level protections (XSS filter, clickjacking prevention, MIME sniffing protection).

Enforced secure cookies over HTTPS.

Enabled CSRF protection for all forms.

Validated and sanitized all user input using Django forms.

Avoided SQL injection through ORM usage.

Implemented a strict Content Security Policy (CSP).

Documented and manually tested all security configurations.

These implementations ensure the Django application follows industry-standard security best practices and is ready for a production environment.
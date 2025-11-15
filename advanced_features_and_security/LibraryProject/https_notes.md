# Django HTTPS and Secure Redirect Configuration

## Overview
This document describes how HTTPS and related security mechanisms were implemented in the LibraryProject to ensure encrypted communication between client and server.

---

## Step 1: HTTPS Enforcement in Django

**Settings configured:**
```python
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
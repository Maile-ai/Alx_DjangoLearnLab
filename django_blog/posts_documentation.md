# Blog Posts — Documentation

## Overview
Adds full CRUD for Post objects:
- List: `/posts/`
- Detail: `/posts/<pk>/`
- Create: `/posts/new/` (auth required)
- Update: `/posts/<pk>/edit/` (author only)
- Delete: `/posts/<pk>/delete/` (author only)

## Permissions
- Anyone can view lists/details.
- Authenticated users can create posts.
- Only the post author can edit/delete (enforced via `UserPassesTestMixin`).

## Setup
1. Add/replace files in the `blog/` app as provided.
2. Run migrations:
   ```bash
   python manage.py makemigrations blog
   python manage.py migrate

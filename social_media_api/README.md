# 🖧 Social Media API

A RESTful backend for a social media platform built with Django and Django REST Framework (DRF).  
This API supports user authentication, posting, commenting, following other users, and retrieving a personalized feed.

---

# 🚀 Features

## 👤 User Management
- Register new users  
- Login with token authentication  
- Update user profile  
- Upload profile pictures  

## 📝 Posts & Comments
- Create, view, update, delete posts  
- Add comments to posts  
- Ownership permissions (users can only edit or delete their own posts & comments)

## 👥 Follow System
- Users can follow or unfollow others  
- Followers and following stored in a many-to-many relationship  
- Feed shows posts from followed users only

## 📰 Personalized Feed
- Authenticated users see posts ONLY from users they follow  
- Feed sorted by newest posts first  

---

# 🔧 Tech Stack

Backend Framework: Django 5 + Django REST Framework  
Authentication: Token Authentication  
Database: SQLite  
Image Uploads: Django media storage  
Pagination & Filtering: DRF built-in  

---

# 📦 Installation

1. Clone the repo  
   git clone <your-repo-url>  
   cd social_media_api  

2. Create a virtual environment  
   python -m venv env  
   source env/bin/activate        (Linux/Mac)  
   env\Scripts\activate           (Windows)

3. Install dependencies  
   pip install -r requirements.txt  

4. Run migrations  
   python manage.py migrate  

5. Start the development server  
   python.manage.py runserver  

API will run at:  
http://127.0.0.1:8000/

---

# 🔐 Authentication (Token Based)

Register:  
POST /api/accounts/register/

Login:  
POST /api/accounts/login/

Example login response:
{
  "message": "Login successful",
  "token": "<your_token>",
  "username": "john"
}

Use token in all protected endpoints:
Authorization: Token <your_token>

---

# 📂 Endpoints Summary

## User Endpoints
POST /api/accounts/register/ — Register (No Auth)  
POST /api/accounts/login/ — Login (No Auth)  
GET /api/accounts/profile/ — View profile (Auth)  
PUT /api/accounts/profile/ — Update profile (Auth)  
POST /api/accounts/follow/<id>/ — Follow user (Auth)  
POST /api/accounts/unfollow/<id>/ — Unfollow user (Auth)  

---

## Posts Endpoints
GET /api/posts/ — List posts  
POST /api/posts/ — Create post (Auth)  
GET /api/posts/<id>/ — View post  
PUT /api/posts/<id>/ — Edit post (Owner Only)  
DELETE /api/posts/<id>/ — Delete post (Owner Only)

---

## Comments Endpoints
POST /api/comments/ — Create comment (Auth)  
GET /api/comments/ — List comments  
PUT /api/comments/<id>/ — Update comment (Owner Only)  
DELETE /api/comments/<id>/ — Delete comment (Owner Only)

---

# 📰 Feed Endpoint

GET /api/feed/  
Authorization: Token <token>

Example:
[
  {
    "id": 2,
    "author": "userB1",
    "title": "Hello from userB1",
    "content": "This is userB1’s first post!"
  }
]

If following no one: []

---

# 🧪 Manual Testing (Step 5 Verified)

1. Register userA and userB  
2. userB logs in and creates a post  
3. userA logs in and follows userB  
4. userA requests GET /api/feed/ → sees userB's posts  

---

# 📁 Project Structure

accounts/  
- models.py  
- serializers.py  
- views.py  
- urls.py  

posts/  
- models.py  
- serializers.py  
- views.py  
- urls.py  

social_media_api/  
- settings.py  
- urls.py  

manage.py  
README.md  

---

# 🎉 Final Notes

This API provides a solid backend foundation for social apps.  
Easily extendable with likes, notifications, messaging, or Swagger docs.  

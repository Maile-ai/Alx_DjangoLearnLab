Managing Permissions and Groups in Django

Project Overview
This project demonstrates how to **manage permissions and groups in Django** to implement **role-based access control (RBAC)**.  
It is part of the **Advanced Features and Security** module of the Library Project.

The goal was to build a secure system that restricts what each user can do based on their assigned **group (role)**.

Objective
To implement and manage **permissions and groups** within a Django application to control user access to specific actions such as viewing, creating, editing, and deleting books.



Project Structure
LibraryProject/
│
├── LibraryProject/ # main project folder
│ └── urls.py # includes bookshelf.urls
│
├── bookshelf/ # app handling books and users
│ ├── models.py # Book model + CustomUser
│ ├── views.py # CRUD views protected by permissions
│ ├── urls.py # route definitions for all book views
│ ├── admin.py # registers CustomUser and Book
│ └── templates/
│ └── bookshelf/
│ ├── book_list.html
│ ├── create_book.html
│ ├── edit_book.html
│ ├── delete_book.html
│ └── success.html
│
└── relationship_app/ 


Core Features

* Custom User Model
- Extended from `AbstractUser`
- Added fields: `date_of_birth`, `profile_photo`
- Uses a custom manager (`CustomUserManager`)

* Custom Model Permissions
 Defined in the `Book` model:

class Meta:
    permissions = [
        ('can_view', 'Can view book'),
        ('can_create', 'Can create book'),
        ('can_edit', 'Can edit book'),
        ('can_delete', 'Can delete book'),
    ]
* Role-Based Groups
Created via Django shell and admin:

Group	Permissions
Viewers	can_view
Editors	can_view, can_create, can_edit
Admins	can_view, can_create, can_edit, can_delete

* Permission-Protected Views
Each view uses:

python
@login_required
@permission_required('bookshelf.permission_name', raise_exception=True)
Views include:

book_list → view all books

create_book → add books

edit_book → update books

delete_book → remove books

* Simple HTML Templates
Basic templates for each operation inside:

bookshelf/templates/bookshelf/
Each template is plain HTML, focused on demonstrating functionality and permission control.

Testing Access Control
Role	Can View	Can Create	Can Edit	Can Delete
Viewers	✅	❌	❌	❌
Editors	✅	✅	✅	❌
Admins	✅	✅	✅	✅

*How to Run the Project

Clone the repository

git clone <your_repo_url>
cd LibraryProject
Run migrations

python manage.py makemigrations
python manage.py migrate
Create a superuser

python manage.py createsuperuser
Start the server

python manage.py runserver

Log in at:
http://127.0.0.1:8000/admin/

Outcomes
Implemented custom permissions and user roles.

Protected all CRUD views with appropriate permission checks.

Fully functional authentication and access control flow.

Ready for expansion into a real-world Django web app.

👩🏽‍💻 Author
Mokete Maile


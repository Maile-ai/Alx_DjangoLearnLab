from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # Function-based registration view
    path('register/', views.register, name='register'),

    # Login view using Django's built-in LoginView
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),

    # Logout view using Django's built-in LogoutView
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    
    path('admin_view/', views.admin_view, name='admin_view'),
    
    path('librarian_view/', views.librarian_view, name='librarian_view'),
    
    path('member_view/', views.member_view, name='member_view'),

    path('role_redirect/', views.role_redirect_view, name='role_redirect'),

    path('add_book/', views.add_book_view, name='add_book'),
    
    path('edit_book/', views.edit_book_view, name='edit_book'),
    
    path('delete_book/', views.delete_book_view, name='delete_book'),
]
from django.urls import path
from .views import book_list, LibraryDetailView

urlpatterns = [
    # Function-based view: lists all books
    path('books/', book_list, name='book_list'),

    # Class-based view: shows details for a specific library
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
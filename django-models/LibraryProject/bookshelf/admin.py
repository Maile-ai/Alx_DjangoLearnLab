from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Display these columns in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Add filter options in the right sidebar
    list_filter = ('publication_year',)
    
    # Enable search bar to search by title or author
    search_fields = ('title', 'author')
# Register your models here.

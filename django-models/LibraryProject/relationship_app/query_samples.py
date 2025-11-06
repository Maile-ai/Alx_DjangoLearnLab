import os
import sys
import django

# --- Setup Django environment ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# -------------------------------
# 1️⃣ Query all books by a specific author
# -------------------------------
author_name = "J.K. Rowling"

try:
    author = Author.objects.get(name=author_name)
    # Forward relationship: Author → Book
    books_by_author = author.book_set.all()
    print(f"\nBooks by {author.name}:")
    for book in books_by_author:
        print(f" - {book.title}")
except Author.DoesNotExist:
    print(f"No author found with name '{author_name}'.")


# -------------------------------
# 2️⃣ List all books in a library
# -------------------------------
library_name = "City Central Library"

try:
    library = Library.objects.get(name=library_name)
    # Reverse relationship: Library → Book (via related_name or default: book_set)
    books_in_library = library.book_set.all()  # You could also use .books.all() if defined in model
    print(f"\nBooks in {library.name}:")
    for book in books_in_library:
        print(f" - {book.title} by {book.author.name}")
except Library.DoesNotExist:
    print(f"No library found with name '{library_name}'.")
    library = None  # avoid NameError later


# -------------------------------
# 3️⃣ Retrieve the librarian for a library
# -------------------------------
if library:
    try:
        librarian = library.librarian  # Reverse OneToOneField access
        print(f"\nLibrarian for {library.name}: {librarian.name}")
    except Librarian.DoesNotExist:
        print(f"No librarian found for {library.name}.")
else:
    print("\nSkipping librarian query because the library does not exist.")
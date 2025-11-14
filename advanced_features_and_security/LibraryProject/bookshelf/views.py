from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        Book.objects.create(title=title, author=author, publication_year=publication_year)
        return render(request, 'bookshelf/success.html')
    return render(request, 'bookshelf/create_book.html')

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.publication_year = request.POST.get('publication_year')
        book.save()
        return render(request, 'bookshelf/success.html')
    return render(request, 'bookshelf/edit_book.html', {'book': book})

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        book.delete()
        return render(request, 'bookshelf/success.html')
    return render(request, 'bookshelf/delete_book.html', {'book': book})
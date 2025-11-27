# Advanced API Project

## Book API Endpoints

### CRUD Views
- GET /books/ → list books
- GET /books/<pk>/ → retrieve book
- POST /books/create/ → create book
- PUT /books/<pk>/update/ → update book
- DELETE /books/<pk>/delete/ → delete book

### Permissions
- Public: List & Detail
- Authenticated Only: Create, Update, Delete

### Filtering Examples
/books/?title=Python  
/books/?author=1  
/books/?publication_year=2023

### Search Examples
/books/?search=django

### Ordering Examples
/books/?ordering=title  
/books/?ordering=-publication_year
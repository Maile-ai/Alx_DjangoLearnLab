**Project Overview**

- **What:** A small Django 5.2 API project (`advanced_api_project`) with a single app `api` that models `Author` and `Book` (see `api/models.py`). It uses Django REST Framework (`rest_framework` in `INSTALLED_APPS`).
- **Why:** The app demonstrates basic relational models, nested serialization, and serializer-level validation.

**Key Files & Patterns**

- `advanced_api_project/settings.py`: core settings. Note `INSTALLED_APPS` includes `rest_framework` and `api`.
- `manage.py`: standard Django command entrypoint for running servers, migrations, and tests.
- `advanced_api_project/urls.py`: currently only registers the admin; API routes should be added here (or include `api/urls.py`).
- `api/models.py`: defines `Author` and `Book`. `Book.author` uses `related_name='books'` (used by serializers).
- `api/serializers.py`: uses `ModelSerializer`. Example patterns:
  - `BookSerializer` validates `publication_year` with `validate_publication_year` (serializer field validator naming convention: `validate_<field>`).
  - `AuthorSerializer` nests `BookSerializer` with `books = BookSerializer(many=True, read_only=True)`.
- `api/views.py`: currently empty and contains a broken import (`from djang`) — fix before implementing endpoints. Preferred approach is to use DRF viewsets / generic views and route them with a `DefaultRouter` in `api/urls.py`.
- `api/migrations/0001_initial.py`: auto-generated schema; authoritative source for current DB shape.

**Developer Workflows (PowerShell / Windows)**

- Create & activate a virtualenv (recommended):

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

- Install deps (project uses Django and djangorestframework):

```
pip install django djangorestframework
```

- Run the dev server:

```
python manage.py migrate
python manage.py runserver
```

- Create a superuser for admin access:

```
python manage.py createsuperuser
```

- Run tests:

```
python manage.py test
```

**Project-specific Conventions & Notes for an AI agent**

- Routing: The top-level `urls.py` currently lacks API includes. When adding endpoints, create `api/urls.py` and include it from `advanced_api_project/urls.py` (e.g., `path('api/', include('api.urls'))`). Prefer DRF `routers.DefaultRouter()` + `ViewSet`s for consistent endpoints.
- Serializers: Use `ModelSerializer` and put per-field validation in `validate_<field>` methods as in `api/serializers.py`.
- Related objects: Use the `related_name` (e.g., `author.books`) rather than reverse queries; serializers already expose `books` as nested read-only.
- Database: SQLite is configured in `settings.py` using `BASE_DIR / 'db.sqlite3'`. Migrations are present and should be kept in sync.
- Tests: `api/tests.py` is currently empty — new tests should use Django `TestCase` or DRF `APITestCase`. Look for patterns in the codebase and keep tests focused on serializer validation and view behavior.

**Common Tasks & Examples**

- Add a simple ViewSet for `Book` (example):

```py
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

- Hooking the ViewSet into URLs (`api/urls.py` example):

```py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

- Then include `api` urls in `advanced_api_project/urls.py`:

```py
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```

**Known Issues & Attention Points**

- `api/views.py` currently has a broken import (`from djang`) and no views implemented. Fix that file before running server or creating routes.
- `advanced_api_project/urls.py` doesn't include `api` routes — APIs will be unreachable until that's added.
- `SECRET_KEY` is present in `settings.py` and `DEBUG=True` — this is fine for local development but treat as sensitive for production.

**Integration Points / External Dependencies**

- External libs: `django`, `djangorestframework`. There are no external web services or third-party APIs configured in this repo.
- DB: SQLite (file `db.sqlite3`) is used for local dev.

**When in doubt — minimal, safe changes**

- Prefer small, focused PRs: (1) fix `api/views.py`, (2) add `api/urls.py` + router, (3) register routes in project `urls.py`, (4) implement tests for serializer validation.
- Run `python manage.py migrate` after model changes and update migrations with `python manage.py makemigrations`.

If any of these notes are unclear or you want the agent to implement a specific endpoint, tests, or CI config, say which task and I will proceed.

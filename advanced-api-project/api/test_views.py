from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Book, Author
from .serializers import BookSerializer


class BookAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="tester", password="testpass123"
        )
        self.client.login(username="tester", password="testpass123")

        self.author = Author.objects.create(
            name="Test Author"
        )

        self.book1 = Book.objects.create(
            title="Python Basics",
            author=self.author,
            publication_year=2020
        )
        self.book2 = Book.objects.create(
            title="Advanced Django",
            author=self.author,
            publication_year=2021
        )

    def test_list_books(self):
        url = reverse("book-list")
        response = self.client.get(url)
        books = Book.objects.order_by("title")
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_book(self):
        url = reverse("book-detail", args=[self.book1.id])
        response = self.client.get(url)
        serializer = BookSerializer(self.book1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_book(self):
        url = reverse("book-create")
        payload = {
            "title": "New Test Book",
            "author": self.author.id,
            "publication_year": 2023
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.last().title, "New Test Book")

    def test_update_book(self):
        url = reverse("book-update", args=[self.book1.id])
        payload = {
            "title": "Updated Title",
            "author": self.author.id,
            "publication_year": 2020
        }
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    def test_delete_book(self):
        url = reverse("book-delete", args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_filter_books(self):
        url = "/api/books/?publication_year=2020"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books(self):
        url = "/api/books/?search=Python"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books(self):
        url = "/api/books/?ordering=-publication_year"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["publication_year"], 2021)

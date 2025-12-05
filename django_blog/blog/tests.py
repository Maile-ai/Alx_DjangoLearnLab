# blog/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

class PostTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="author", email="a@example.com", password="passw0rd")
        self.other = User.objects.create_user(username="other", password="passw0rd")
        self.post = Post.objects.create(title="Test post", content="Content here", author=self.user)

    def test_list_view_accessible(self):
        resp = self.client.get(reverse('posts'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.post.title)

    def test_detail_view(self):
        resp = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.post.title)

    def test_create_requires_auth(self):
        resp = self.client.get(reverse('post-create'))
        self.assertEqual(resp.status_code, 302)  # redirect to login
        self.client.login(username='author', password='passw0rd')
        resp = self.client.post(reverse('post-create'), {'title': 'New', 'content': 'body'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Post.objects.filter(title='New').exists())

    def test_update_by_author_only(self):
        url = reverse('post-update', kwargs={'pk': self.post.pk})
        self.client.login(username='other', password='passw0rd')
        resp = self.client.get(url)
        self.assertIn(resp.status_code, (302, 403))
        self.client.login(username='author', password='passw0rd')
        resp = self.client.post(url, {'title': 'Updated', 'content': 'x'}, follow=True)
        self.assertContains(resp, 'Updated')

    def test_delete_by_author_only(self):
        url = reverse('post-delete', kwargs={'pk': self.post.pk})
        self.client.login(username='other', password='passw0rd')
        resp = self.client.post(url)
        self.assertIn(resp.status_code, (302, 403))
        self.client.login(username='author', password='passw0rd')
        resp = self.client.post(url, follow=True)
        self.assertRedirects(resp, reverse('posts'))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

from django.test import TestCase
from django.urls import reverse
from portfolio.models import Project, Post

class ViewTests(TestCase):
    def setUp(self):
        Project.objects.create(title="Test Project", slug="test-project", content="Body")
        Post.objects.create(title="Test Post", slug="test-post", body="Some content", published=True)

    def test_home(self):
        r = self.client.get(reverse("portfolio:home"))
        self.assertEqual(r.status_code, 200)

    def test_projects(self):
        r = self.client.get(reverse("portfolio:projects"))
        self.assertContains(r, "Projects")

    def test_project_detail(self):
        r = self.client.get(reverse("portfolio:project_detail", args=["test-project"]))
        self.assertEqual(r.status_code, 200)

    def test_blog_index(self):
        r = self.client.get(reverse("portfolio:blog"))
        self.assertEqual(r.status_code, 200)

    def test_post_detail(self):
        r = self.client.get(reverse("portfolio:post_detail", args=["test-post"]))
        self.assertEqual(r.status_code, 200)

    def test_search_json(self):
        r = self.client.get(reverse("portfolio:search_json"), {"q": "test"})
        self.assertEqual(r.status_code, 200)
        self.assertIn("posts", r.json())
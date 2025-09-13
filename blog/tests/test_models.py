from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Post, Category

class PostModelTests(TestCase):
    def setUp(self):
        self.u = User.objects.create_user("alice","a@a.com","pass")
        self.cat = Category.create(name="News", slug="news") if hasattr(Category, "create") \
            else Category.objects.create(name="News", slug="news")

    def test_slug_autogenerates(self):
        p = Post.objects.create(title="Hello World", author=self.u, category=self.cat, body="<p>Body</p>", status="published")
        self.assertTrue(p.slug)

    def test_status_default_is_draft(self):
        p = Post.objects.create(title="Drafty", author=self.u, category=self.cat, body="<p>Body</p>")
        self.assertEqual(p.status, Post.Status.DRAFT)

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post, Category

class CommentPermissionsTests(TestCase):
    def setUp(self):
        self.u = User.objects.create_user("sam","s@s.com","pass")
        self.cat = Category.objects.create(name="Gen", slug="gen")
        self.post = Post.objects.create(title="P", author=self.u, category=self.cat, body="<p>x</p>", status="published")

    def test_comment_requires_login(self):
        r = self.client.post(reverse("blog:add_comment", args=[self.post.slug]), {"body": "Hi"})
        self.assertEqual(r.status_code, 302)  # redirected to login

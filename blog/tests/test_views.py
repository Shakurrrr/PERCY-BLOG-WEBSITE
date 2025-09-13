from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post, Category

class PostListTests(TestCase):
    def setUp(self):
        self.u = User.objects.create_user("bob","b@b.com","pass")
        self.cat = Category.objects.create(name="Tech", slug="tech")
        for i in range(15):
            Post.objects.create(title=f"Post {i}", author=self.u, category=self.cat,
                                body="<p>Body</p>", status="published")

    def test_pagination(self):
        r = self.client.get(reverse("blog:post_list"))
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.context["page_obj"].has_next())

    def test_search_icontains(self):
        r = self.client.get(reverse("blog:post_list"), {"q": "Post 1"})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Post 1")

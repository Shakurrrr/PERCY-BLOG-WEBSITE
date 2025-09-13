from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post

class LatestPostsFeed(Feed):
    title = "Latest Posts"
    link = "/"
    description = "Recent articles."

    def items(self):
        return Post.objects.filter(status="published").order_by("-published_at")[:20]

    def item_title(self, item): return item.title
    def item_description(self, item): return item.excerpt or ""
    def item_link(self, item): return reverse("blog:post_detail", args=[item.slug])

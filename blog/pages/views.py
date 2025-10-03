from django.shortcuts import render
from blog.models import Post

def landing(request):
    latest = Post.objects.published().order_by("-published_at")[:6] \
             if hasattr(Post.objects, "published") else Post.objects.order_by("-id")[:6]
    return render(request, "landing.html", {"latest_posts": latest})

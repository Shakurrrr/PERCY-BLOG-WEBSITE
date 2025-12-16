from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Category, Tag, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm
from django.shortcuts import render, redirect
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import MyTokenObtainPairSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAuthorOrReadOnly
from .models import Post
from .serializers import PostSerializer



def _published_qs():
    return Post.objects.filter(status=Post.Status.PUBLISHED)

def post_list(request, slug=None):
    qs = _published_qs().select_related("author","category").prefetch_related("tags")
    category = tag = None

    if "q" in request.GET:
        q = request.GET.get("q","").strip()
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(excerpt__icontains=q) |
                Q(body__icontains=q) |
                Q(category__name__icontains=q) |
                Q(tags__name__icontains=q)
            ).distinct()

    if request.resolver_match.url_name == "post_by_category":
        category = get_object_or_404(Category, slug=slug)
        qs = qs.filter(category=category)
    if request.resolver_match.url_name == "post_by_tag":
        tag = get_object_or_404(Tag, slug=slug)
        qs = qs.filter(tags=tag)

    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "blog/post_list.html", {"page_obj": page_obj, "category": category, "tag": tag})
     

def post_detail(request, slug):
    post = get_object_or_404(_published_qs().select_related("author","category"), slug=slug)
    comments = post.comments.filter(is_approved=True).select_related("user")
    form = CommentForm()
    return render(request, "blog/post_detail.html", {"post": post, "comments": comments, "form": form})

@login_required
@permission_required("blog.add_post", raise_exception=True)
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.author = request.user
        obj.save()
        form.save_m2m()
        messages.success(request, "Post created.")
        return redirect("blog:post_detail", slug=obj.slug)
    return render(request, "blog/post_form.html", {"form": form})

@login_required
@permission_required("blog.change_post", raise_exception=True)
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user != post.author and not request.user.has_perm("blog.change_post"):
        messages.error(request, "Not authorized.")
        return redirect("blog:post_detail", slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Post updated.")
        return redirect("blog:post_detail", slug=post.slug)
    return render(request, "blog/post_form.html", {"form": form})

@login_required
@permission_required("blog.delete_post", raise_exception=True)
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    messages.success(request, "Post deleted.")
    return redirect("blog:post_list")

@login_required
@permission_required("blog.add_comment", raise_exception=True)
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLISHED)
    form = CommentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        c = form.save(commit=False)
        c.user = request.user
        c.post = post
        c.save()
        messages.success(request, "Comment added.")
    return redirect("blog:post_detail", slug=slug)

def signup(request):
    if request.user.is_authenticated:
        return redirect("blog:post_list")
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        login(request, user)
        return redirect("blog:post_list")
    return render(request, "registration/signup.html", {"form": form})

# JWT with cookies

class CookieLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        u = authenticate(
            request,
            username=request.data.get("username"),
            password=request.data.get("password"),
        )
        if not u:
            return Response({"detail": "Invalid credentials"}, status=400)

        refresh = RefreshToken.for_user(u)
        access = str(refresh.access_token)

        resp = Response({"detail": "ok"})
        # set cookies
        resp.set_cookie(
            "access_token", access,
            max_age=15*60, httponly=True, secure=not settings.DEBUG,
            samesite="Lax", path="/"
        )
        resp.set_cookie(
            "refresh_token", str(refresh),
            max_age=7*24*3600, httponly=True, secure=not settings.DEBUG,
            samesite="Lax", path="/api/auth/"
        )
        return resp

class CookieLogout(APIView):
    def post(self, request):
        resp = Response({"detail": "logged out"})
        resp.delete_cookie("access_token", path="/")
        resp.delete_cookie("refresh_token", path="/api/auth/")
        return resp
    

  
class MyTokenObtainPairView(TokenObtainPairView):
     serializer_class = MyTokenObtainPairSerializer



class PostViewSet(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


def landing(request):
    latest_posts = Post.objects.published().order_by("-published_at")[:6] \
        if hasattr(Post.objects, "published") else Post.objects.filter(status="published").order_by("-published_at")[:6]
    return render(request, "landing.html", {"latest_posts": latest_posts})

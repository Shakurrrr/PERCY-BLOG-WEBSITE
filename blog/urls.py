from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from blog.api import Me
from .views_auth import CookieLogin, CookieLogout
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views



app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("api/me/", Me.as_view()),

    # most important route FIRST
    path("post/create/", views.post_create, name="post_create"),
    path("post/<slug:slug>/edit/", views.post_edit, name="post_edit"),
    path("post/<slug:slug>/delete/", views.post_delete, name="post_delete"),
    path("post/<slug:slug>/comment/", views.add_comment, name="add_comment"),

    path("blog/", views.post_list, name="post_list"),  # now /blog/
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),


    path("api/auth/login/",  CookieLogin.as_view(),  name="cookie-login"),
    path("api/auth/logout/", CookieLogout.as_view(), name="cookie-logout"),

    # Filters
    path("category/<slug:slug>/", views.post_list, name="post_by_category"),
    path("tag/<slug:slug>/", views.post_list, name="post_by_tag"),

    # Auth/Signup
    path("signup/", views.signup, name="signup"),

    # JWT Authentication
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/auth/login/", CookieLogin.as_view()),
    path("api/auth/logout/", CookieLogout.as_view()),

]




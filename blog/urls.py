from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="post_list"),

    # Specific routes FIRST
    path("post/create/", views.post_create, name="post_create"),
    path("post/<slug:slug>/edit/", views.post_edit, name="post_edit"),
    path("post/<slug:slug>/delete/", views.post_delete, name="post_delete"),
    path("post/<slug:slug>/comment/", views.add_comment, name="add_comment"),

    # Filters
    path("category/<slug:slug>/", views.post_list, name="post_by_category"),
    path("tag/<slug:slug>/", views.post_list, name="post_by_tag"),

    # Catch-all detail LAST
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),

    # Auth/Signup
    path("signup/", views.signup, name="signup"),
]

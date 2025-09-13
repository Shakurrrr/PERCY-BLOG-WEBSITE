from django.contrib import admin
from .models import Post, Category, Tag, Comment
from django.db import models

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title","author","category","status","published_at","created_at")
    list_filter = ("status","category","tags","author")
    search_fields = ("title","excerpt","body")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("author","category","tags")
    date_hierarchy = "published_at"
    ordering = ("-published_at",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ("name","slug","created_at")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ("name","slug","created_at")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post","user","is_approved","created_at")
    list_filter = ("is_approved",)
    search_fields = ("body",)
    autocomplete_fields = ("post","user")


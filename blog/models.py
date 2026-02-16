from django.conf import settings
from django.db import models
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector

# My model being created here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
    
class Category(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    def __str__(self): return self.name

class Tag(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True)
    def __str__(self): return self.name

class Post(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="posts")
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    excerpt = models.CharField(max_length=300, blank=True)
    body = RichTextUploadingField()  # CKEditor rich text
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(null=True, blank=True)
    featured_image = models.ImageField(upload_to="post_images/", blank=True, null=True)

    class Meta:
        ordering = ["-published_at","-created_at"]
        

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self): return self.title

class Comment(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    is_approved = models.BooleanField(default=True)  # simple moderation toggle
    def __str__(self): return f"Comment by {self.user} on {self.post}"

    
class PostTag(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'tag')
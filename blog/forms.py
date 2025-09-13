# blog/forms.py
from django import forms
from django.forms import ClearableFileInput
from django.contrib.auth.models import User
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Post, Comment

class PostForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorUploadingWidget())
    featured_image = forms.ImageField(
        required=False,
        widget=ClearableFileInput(attrs={"accept": "image/*", "class": "block w-full"})
    )

    class Meta:
        model = Post
        fields = [
            "title", "excerpt", "category", "tags",
            "featured_image", "body", "status", "published_at"
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]

class SignupForm(forms.ModelForm):
    """
    Simple signup form to match your current view logic:
    - uses a single 'password' field (view calls set_password on it)
    If you want password confirmation, we can swap to UserCreationForm later.
    """
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        widgets = {
            "username": forms.TextInput(attrs={"autocomplete": "username"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
        }

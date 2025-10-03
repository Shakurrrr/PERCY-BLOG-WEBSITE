# blog/serializers.py
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# ---- JWT (already needed) ----
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["is_staff"] = user.is_staff
        return token

# ---- Blog serializers ----
# Adjust the import if your model is named differently (e.g., Article)
from .models import Post  # <-- make sure this model exists

class PostSerializer(serializers.ModelSerializer):
    # Optional nice representations:
    author = serializers.StringRelatedField(read_only=True)  # shows username if __str__ on User
    # If you have M2M tags or FK category and want IDs instead, you can omit the two lines below.
    # tags = serializers.SlugRelatedField(slug_field="name", many=True, read_only=True)
    # category = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Post
        fields = "__all__"   # simplest; includes every field on Post
        read_only_fields = ("id", "created_at", "updated_at")  # adjust to your model

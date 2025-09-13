# blog/context_processors.py
from .models import Category, Tag

def menu_data(request):
    # Small, cheap queries for navbar menus
    return {
        "nav_categories": Category.objects.only("id", "name", "slug").order_by("name")[:10],
        "nav_tags": Tag.objects.only("id", "name", "slug").order_by("name")[:15],
    }

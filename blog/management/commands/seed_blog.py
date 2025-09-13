# blog/management/commands/seed_blog.py
import os, random, urllib.request
from pathlib import Path
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from blog.models import Category, Tag, Post

CATS = ["Tech", "Business", "Design", "AI", "DevOps"]
TAGS = ["django", "python", "tailwind", "cloud", "postgres", "tips", "howto"]

def get_or_create_category(name: str) -> Category:
    slug = slugify(name)
    obj, _ = Category.objects.get_or_create(slug=slug, defaults={"name": name})
    # Keep display name in sync (optional)
    if obj.name != name:
        obj.name = name
        obj.save(update_fields=["name"])
    return obj

def get_or_create_tag(name: str) -> Tag:
    slug = slugify(name)
    obj, _ = Tag.objects.get_or_create(slug=slug, defaults={"name": name})
    if obj.name != name:
        obj.name = name
        obj.save(update_fields=["name"])
    return obj

class Command(BaseCommand):
    help = "Seed categories, tags, and posts with featured images (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=12)

    def handle(self, *args, **opts):
        count = opts["count"]

        # Author
        author, _ = User.objects.get_or_create(
            username="demo_author", defaults={"email": "demo@example.com"}
        )
        if not author.has_usable_password():
            author.set_password("demo12345")
            author.save(update_fields=["password"])

        cats = [get_or_create_category(c) for c in CATS]
        tags = [get_or_create_tag(t) for t in TAGS]

        media_root = Path(os.getenv("MEDIA_ROOT", "media"))
        img_dir = media_root / "post_images"
        img_dir.mkdir(parents=True, exist_ok=True)

        created = 0
        for i in range(count):
            title = f"Sample Post {i+1}"
            slug = slugify(title)

            post, was_created = Post.objects.get_or_create(
                slug=slug,
                defaults={
                    "title": title,
                    "author": author,
                    "category": random.choice(cats),
                    "excerpt": "This is a seeded post for UI testing.",
                    "body": "<p>Lorem ipsum dolor sit amet. <strong>Django</strong> + CKEditor demo content.</p>",
                    "status": Post.Status.PUBLISHED,
                    "published_at": timezone.now(),
                },
            )
            # Attach tags (1–3)
            pick = random.sample(tags, k=random.randint(1, 3))
            post.tags.add(*pick)

            # Feature image (only if missing)
            if not post.featured_image:
                img_path = img_dir / f"{slug}.jpg"
                try:
                    urllib.request.urlretrieve(
                        f"https://picsum.photos/seed/{slug}/1200/800", img_path
                    )
                    with open(img_path, "rb") as fh:
                        post.featured_image.save(img_path.name, File(fh), save=True)
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Image fetch failed: {e}"))

            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Seed complete. Created {created} posts."))

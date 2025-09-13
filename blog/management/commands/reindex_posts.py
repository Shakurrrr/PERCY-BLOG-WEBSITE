from django.core.management.base import BaseCommand
from blog.models import Post
from blog.search import INDEX, serialize_post

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        docs = [serialize_post(p) for p in Post.objects.filter(status="published").prefetch_related("tags","category")]
        INDEX.delete_all_documents()
        if docs: INDEX.add_documents(docs)
        self.stdout.write(self.style.SUCCESS(f"Indexed {len(docs)} posts"))

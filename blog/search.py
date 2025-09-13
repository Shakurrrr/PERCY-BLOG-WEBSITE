import os, meilisearch
client = meilisearch.Client(os.getenv("MEILI_URL","http://127.0.0.1:7700"), os.getenv("MEILI_KEY","masterKey"))
INDEX = client.index("posts")

def serialize_post(p):
    return {
        "id": p.id, "title": p.title, "excerpt": p.excerpt,
        "body": p.body, "slug": p.slug,
        "category": p.category.name, "tags": [t.name for t in p.tags.all()],
        "published_at": p.published_at.isoformat() if p.published_at else None,
    }

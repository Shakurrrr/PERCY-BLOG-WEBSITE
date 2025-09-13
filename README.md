PERCY_BLOG_WEBSITE — Django Blog CMS (CKEditor + Tailwind)

A production-grade, opinionated blog/CMS built on Django 5, with role-based access, rich text editing (CKEditor upload), image handling, search, and a modern Tailwind UI. Designed for rapid content operations and a clean developer experience.

Key Features

Users & Roles: Sign-up/login/password reset; Admin, Editor, Reader groups with scoped permissions.

Content Model: Posts, Categories, Tags, Comments (moderation toggle).

Rich Editor: CKEditor (with uploads) for authoring; image/file uploads to MEDIA_ROOT.

Media: Featured image per post; static/media served in dev, S3-ready in prod.

Search & Pagination: Basic search (icontains) + paginated list view.

Modern UI: Tailwind CSS, responsive layouts, related posts, tag chips, new-post CTA.

Admin: Extended Django admin for content ops.

Seeding: Management command to generate demo content, tags, categories, and images.

Tech Stack

Backend: Django 5.x, Django ORM (SQLite for dev; Postgres recommended in prod)

Editor: django-ckeditor + ckeditor_uploader

Storage (prod-ready): django-storages (S3)

Frontend: Tailwind CSS (compiled), @tailwindcss/forms/typography/line-clamp

Auth: django.contrib.auth flows and themed templates

⚠️ Note on CKEditor 4: The bundled CKEditor 4 in django-ckeditor is EOL for production. Fine for local/dev. For production, plan a migration to CKEditor 5 (e.g., django-ckeditor-5) or TinyMCE.

Project Structure
blogsite/                # Django project settings/urls
blog/                    # App (models, views, forms, urls, templates)
  management/commands/   # seed_blog command
  templates/blog/        # post_list, post_detail, post_form, etc.
templates/               # base.html, registration/* (auth views)
static/                  # static assets (dev)  -> served via collectstatic in prod
  css/app.css            # Tailwind output
assets/                  # tailwind.css (input)
media/                   # user uploads (dev)
ui.preset.js             # Tailwind design tokens preset (your palette/spacing/etc.)
tailwind.config.js       # Tailwind config (Django-aware content paths)
postcss.config.js

Quick Start (Local Dev)
Prerequisites

Python 3.11+ (3.13 ok), Node 18+

Git & (optionally) GitHub CLI

1) Python environment
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux
python -m venv .venv
source .venv/bin/activate


Install deps:

pip install -r requirements.txt  # if present
# or minimum:
pip install django==5.* pillow django-ckeditor django-storages python-dotenv

2) Environment variables

Create .env in the project root:

DJANGO_SECRET_KEY=your-long-secret-key
# Optional S3 (prod)
# AWS_STORAGE_BUCKET_NAME=...
# AWS_S3_REGION_NAME=eu-west-1


Settings expect .env to be loaded (via python-dotenv). If not present in your tree yet, add at the top of blogsite/settings.py:

from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-not-secure")

3) Database & RBAC bootstrap
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser


RBAC groups (Admin/Editor/Reader) are auto-created via a post_migrate signal (on first migrate). Assign users to groups in /admin.

4) Tailwind CSS build

Option A (recommended, cross-platform; no PATH issues)

npm i -D tailwindcss postcss autoprefixer @tailwindcss/forms @tailwindcss/typography @tailwindcss/line-clamp
# Build once:
node ./node_modules/tailwindcss/lib/cli.js -i ./assets/tailwind.css -o ./static/css/app.css
# Dev watch:
node ./node_modules/tailwindcss/lib/cli.js -i ./assets/tailwind.css -o ./static/css/app.css --watch


Option B (PostCSS CLI runner)

npm i -D postcss-cli tailwindcss postcss autoprefixer
npx postcss ./assets/tailwind.css -o ./static/css/app.css --watch

5) Run the server
python manage.py runserver


Open http://127.0.0.1:8000/

Seed Demo Content (optional)

Populate categories, tags, posts with images:

python manage.py seed_blog --count 12


This command is idempotent (uses slug-based get_or_create) and downloads placeholder images for featured covers.

Core URLs

Home / List: /

Search: /?q=term

Filters:

By category: /category/<slug>/

By tag: /tag/<slug>/

Post detail: /post/<slug>/

Create: /post/create/ (Admin/Editor)

Edit/Delete: /post/<slug>/edit/, /post/<slug>/delete/ (role-gated)

Comment: /post/<slug>/comment/ (authenticated)

Auth: /accounts/login/, /accounts/logout/, /accounts/password_reset/ (and friends)

Signup: /signup/

Admin: /admin/

Ordering matters in blog/urls.py: declare post/create, post/<slug>/edit, etc., before the catch-all post/<slug>/.

Configuration Notes

Static/Media (dev):

STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_ROOT = BASE_DIR / "media", MEDIA_URL = "media/"

In urls.py, serve media in DEBUG=True via static(settings.MEDIA_URL, ...)

Storage (prod):

django-storages with S3 is pre-wired behind if not DEBUG: DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

Email (dev):

Console backend (EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend")

Password reset templates under templates/registration/

Context Navigation:

blog.context_processors.menu_data provides nav_categories and nav_tags to the navbar.

RBAC (Groups & Permissions)

Admin: Full CRUD on posts & comments.

Editor: Add/Change/View posts & comments.

Reader: View posts, add comments.

Assign users to groups via /admin → Auth → Groups / Users.

Testing
python manage.py test


Example unit test in blog/tests/test_models.py validates slug autogeneration, etc. Extend with view tests and form validation as needed.

Production Checklist

Use PostgreSQL (recommended). Update DATABASES in settings.py.

Switch editor to CKEditor 5 or TinyMCE for long-term support.

Configure S3 or equivalent for media; set correct bucket policy and cache headers.

Build CSS and collect static:

npm ci
npm run build
python manage.py collectstatic --noinput


Use a real email backend (SES, SendGrid, etc.) for password resets.

Run behind a WSGI/ASGI server (gunicorn/uvicorn) with a real web server (nginx).

Roadmap (Optional Enhancements)

Search:

Phase 1: icontains (default)

Phase 2: PostgreSQL full-text (SearchVector/Rank)

Phase 3: External engine (Meilisearch/Elasticsearch) if scale demands

SEO: Meta tags, OpenGraph, RSS feed (/feed/)

Analytics: Pageview tracking hooks

Image pipeline: Thumbnails, WebP, responsive images

Editor swap: django-ckeditor-5 migration

Developer Ergonomics

Favicon: Drop a file at static/favicon.ico to remove the 404.

Unique Slugs: Utility available in models to guarantee unique slugs with suffixes.

Form UX: File upload preview for featured images; CKEditor upload widget for body.

License

Pick what fits your use case (e.g., MIT). Add a LICENSE file at the repo root.

TL;DR
# Setup
python -m venv venv && .\venv\Scripts\Activate.ps1
pip install django pillow django-ckeditor django-storages python-dotenv
npm i -D tailwindcss postcss autoprefixer @tailwindcss/forms @tailwindcss/typography @tailwindcss/line-clamp
node ./node_modules/tailwindcss/lib/cli.js -i ./assets/tailwind.css -o ./static/css/app.css --watch
python manage.py migrate
python manage.py runserver

# Seed demo content (optional)
python manage.py seed_blog --count 12

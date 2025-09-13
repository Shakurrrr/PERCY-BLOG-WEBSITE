# PERCY_BLOG_WEBSITE — Django Blog CMS (CKEditor + Tailwind)

A production-grade, opinionated **blog/CMS** built on **Django 5**, with role-based access, rich text editing (CKEditor uploads), featured images, search, and a modern Tailwind UI. Designed for rapid content operations and a clean developer experience.

---

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start (Local Dev)](#quick-start-local-dev)
- [Environment Variables](#environment-variables)
- [Database & RBAC](#database--rbac)
- [Tailwind Build](#tailwind-build)
- [Run the Server](#run-the-server)
- [Seed Demo Content](#seed-demo-content)
- [Core URLs](#core-urls)
- [Configuration Notes](#configuration-notes)
- [Testing](#testing)
- [Production Checklist](#production-checklist)
- [Roadmap](#roadmap)
- [Developer Ergonomics](#developer-ergonomics)
- [License](#license)

---

## Features

- **Users & Roles**: Sign-up / login / password reset; groups **Admin**, **Editor**, **Reader** with scoped permissions.
- **Content Model**: Posts, Categories, Tags, Comments (simple moderation toggle).
- **Rich Editor**: CKEditor (with uploads) for authoring; image/file uploads stored under `MEDIA_ROOT`.
- **Media**: Featured image per post; static/media served in dev; S3-ready configuration for prod.
- **Search & Pagination**: Basic `icontains` search + paginated list view.
- **Modern UI**: Tailwind CSS, responsive layouts, related posts, tag chips, new-post CTA.
- **Admin**: Extended Django admin for content ops.
- **Seeding**: Management command to generate demo content (categories, tags, posts, images).

> ⚠️ **CKEditor 4 notice**: `django-ckeditor` bundles CKEditor 4 which is EOL. It’s acceptable for local/dev. For production, plan a migration to **CKEditor 5** (e.g., `django-ckeditor-5`) or TinyMCE.

---

## Tech Stack

- **Backend**: Django 5.x, Django ORM (SQLite for dev; **PostgreSQL** recommended for prod)
- **Editor**: `django-ckeditor` + `ckeditor_uploader`
- **Storage (prod)**: `django-storages` (S3)
- **Frontend**: Tailwind CSS (compiled) + `@tailwindcss/forms`, `@tailwindcss/typography`, `@tailwindcss/line-clamp`
- **Auth**: `django.contrib.auth` flows, themed templates

---

## Project Structure

blogsite/ # Django project (settings, urls)
blog/ # App (models, views, forms, urls, templates)
management/commands/ # seed_blog command
templates/blog/ # post_list, post_detail, post_form, etc.
templates/ # base.html, registration/* (auth views)
static/ # static assets (dev) → served via collectstatic in prod
css/app.css # Tailwind output (generated)
assets/ # tailwind.css (input)
media/ # user uploads (dev)
ui.preset.js # Tailwind design tokens (palette, spacing, etc.)
tailwind.config.js # Tailwind config (Django-aware content paths)
postcss.config.js

yaml
Copy code

---

## Quick Start (Local Dev)

**Prereqs**: Python **3.11+** (3.13 OK), Node **18+**, Git

### 1) Python env

```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
Install deps:

bash
Copy code
# if a requirements.txt exists:
pip install -r requirements.txt

# minimal set:
pip install "django==5.*" pillow django-ckeditor django-storages python-dotenv
Environment Variables
Create .env in the project root:

ini
Copy code
DJANGO_SECRET_KEY=your-long-secret-key

# Optional (prod)
# AWS_STORAGE_BUCKET_NAME=your-bucket
# AWS_S3_REGION_NAME=eu-west-1
Ensure settings load .env (snippet typically present in blogsite/settings.py):

python
Copy code
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-not-secure")
Database & RBAC
bash
Copy code
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
Assign users to Admin/Editor/Reader in /admin.

If you’ve added a post_migrate signal to auto-create groups/permissions, they’ll appear after the first migrate. Otherwise, create groups manually and attach the standard add/change/delete/view permissions for Post and Comment.

Tailwind Build
Option A — direct CLI via Node (robust on Windows)

bash
Copy code
npm i -D tailwindcss postcss autoprefixer \
       @tailwindcss/forms @tailwindcss/typography @tailwindcss/line-clamp

# Build once
node ./node_modules/tailwindcss/lib/cli.js \
  -i ./assets/tailwind.css -o ./static/css/app.css

# Dev watch
node ./node_modules/tailwindcss/lib/cli.js \
  -i ./assets/tailwind.css -o ./static/css/app.css --watch
Option B — PostCSS CLI runner

bash
Copy code
npm i -D postcss-cli tailwindcss postcss autoprefixer
npx postcss ./assets/tailwind.css -o ./static/css/app.css --watch
Run the Server
bash
Copy code
python manage.py runserver
Open http://127.0.0.1:8000/

Seed Demo Content
Populate categories, tags, posts (with images):

bash
Copy code
python manage.py seed_blog --count 12
The command is idempotent (slug-based get_or_create) and attaches placeholder images for covers.

Core URLs
Home / List: /

Search: /?q=term

Filters:

by category: /category/<slug>/

by tag: /tag/<slug>/

Post detail: /post/<slug>/

Create: /post/create/ (Admin/Editor)

Edit/Delete: /post/<slug>/edit/, /post/<slug>/delete/ (role-gated)

Comment: /post/<slug>/comment/ (authenticated)

Auth: /accounts/login/, /accounts/logout/, /accounts/password_reset/ (+ confirm/complete)

Signup: /signup/

Admin: /admin/

Routing tip: In blog/urls.py, declare post/create, post/<slug>/edit, etc. before the catch-all post/<slug>/.

Configuration Notes
Static/Media (dev)

python
Copy code
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "media/"
Serve media in dev (DEBUG=True) within urls.py:

python
Copy code
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  # ...
] + (static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) if settings.DEBUG else [])
Storage (prod)

django-storages with S3 is pre-wired when DEBUG=False:

python
Copy code
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
Set bucket, region, and caching headers via env.

Email (dev)

Console backend:

python
Copy code
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
Password reset templates under templates/registration/.

Navigation Context

blog.context_processors.menu_data supplies nav_categories and nav_tags to the navbar.

Testing
bash
Copy code
python manage.py test
There’s a baseline model test for slug generation (extend with view/form tests as needed).

Production Checklist
DB: Switch to PostgreSQL; update DATABASES in settings.

Editor: Migrate to CKEditor 5 or TinyMCE for long-term support.

Static/Media:

bash
Copy code
npm ci
npm run build           # or use the node CLI shown above
python manage.py collectstatic --noinput
Email: Use a real provider (SES, SendGrid, etc.) for resets.

Deploy: WSGI/ASGI (gunicorn/uvicorn) behind nginx or similar.

Secrets: Use env vars; never commit keys.

Security: Review CSP/HTTPS/ALLOWED_HOSTS; enable secure cookies in prod.

Roadmap
Search:

Phase 1: icontains (default)

Phase 2: PostgreSQL full-text (SearchVector, SearchRank)

Phase 3: External engine (Meilisearch/Elasticsearch) if scale demands

SEO: Meta tags, OpenGraph, RSS (/feed/)

Analytics: Pageview tracking

Images: Thumbnails, WebP, responsive sources

Editor: Migration to django-ckeditor-5

Developer Ergonomics
Favicon: Drop static/favicon.ico to remove the 404.

Unique Slugs: Utility in models to guarantee uniqueness with suffixes.

Form UX: File upload preview for featured images; CKEditor upload widget for the body.

License
MIT

#!/usr/bin/env bash
set -e

# wait for DB if using Postgres
if [ -n "$DATABASE_URL" ]; then
  python - <<'PY'
import time, os, psycopg
url=os.environ["DATABASE_URL"]
for _ in range(30):
    try:
        with psycopg.connect(url) as _c: pass
        break
    except Exception:
        time.sleep(1)
else:
    raise SystemExit("DB did not become ready")
PY
fi

python manage.py migrate --noinput
# collectstatic is safe to skip in dev; keep it tolerant:
python manage.py collectstatic --noinput || true

# gunicorn in production style, fine for dev too
exec gunicorn blogsite.wsgi:application --bind 0.0.0.0:8000 --workers 3

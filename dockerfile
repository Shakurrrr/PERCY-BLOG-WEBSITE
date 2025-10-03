# Dockerfile
FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=120

WORKDIR /app

# Install Python deps with a cache mount (stable + fast)
COPY requirements-dev.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements-dev.txt

# Copy project
COPY . .

# Simple dev entrypoint
RUN printf '#!/bin/sh\nset -e\npython manage.py migrate --noinput\npython manage.py runserver 0.0.0.0:8000\n' > /entrypoint.sh \
 && chmod +x /entrypoint.sh

EXPOSE 8000
CMD ["/entrypoint.sh"]

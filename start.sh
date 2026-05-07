#!/bin/bash
set -e

# Collect static files
python manage.py collectstatic --noinput --clear

# Run migrations
python manage.py migrate --noinput

# Create default superuser if not exists
python manage.py shell <<'PYEOF'
from django.contrib.auth import get_user_model
import os

User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(
        os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin"),
        os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@enerpulse.com"),
        os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin123")
    )
    print("Superuser created")
else:
    print("Superuser already exists")
PYEOF

# Start gunicorn
exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120

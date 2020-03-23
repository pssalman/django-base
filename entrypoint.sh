#!/bin/sh

export DJANGO_SETTINGS_MODULE=conf.settings.${ENV}

python -c "import django; print('django version:', django.get_version())"
python manage.py wait_for_db
#python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate --no-input
# python manage.py create_super --username command --email command@line.com --password 12345678
python manage.py create_super

python manage.py collectstatic --no-input

python manage.py compilemessages

# Prepare log files and start outputting logs to stdout
touch ./logs/gunicorn/gunicorn-${ENV}.log
touch ./logs/gunicorn/gunicorn-access-${ENV}.log
tail -n 0 -f ./logs/gunicorn/gunicorn*.log &

echo Starting Gunicorn.

exec gunicorn conf.wsgi:application \
    --name webapp_django \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 3 \
    --log-level=info \
    --log-file=./logs/gunicorn/gunicorn-${ENV}.log \
    --access-logfile=./logs/gunicorn/gunicorn-access-${ENV}.log
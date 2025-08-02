web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn settings:application --bind 0.0.0.0:$PORT

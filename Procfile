release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input

web: gunicorn my_e2e_project.wsgi
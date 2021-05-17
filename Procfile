release: python manage.py migrate
#tasks: celery -A penduraai worker -l info
web: daphne penduraai.asgi:application -p 8888

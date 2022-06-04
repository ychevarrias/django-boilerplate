web: gunicorn webapp.wsgi --log-file -
celery: celery -A webapp worker -n celery@devlab.local2 --loglevel=INFO
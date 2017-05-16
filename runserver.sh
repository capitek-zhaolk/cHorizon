#python manage.py migrate_settings --gendiff
#tox -e manage -- compilemessages

tox -e runserver -- 0.0.0.0:80

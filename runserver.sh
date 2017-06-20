#python manage.py migrate_settings --gendiff

rm -rf static/dashboard/js/*

tox -e manage -- compilemessages

tox -e runserver -- 0.0.0.0:80

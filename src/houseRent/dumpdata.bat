@echo off
python manage.py dumpdata --indent 4 > populate.json

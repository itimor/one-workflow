#!/bin/bash

apps=(systems tools notices workflows tickets)
rm -rf core.db
for app in ${apps[@]};do
  rm -rf $app/migrations
done

for app in ${apps[@]};do
  echo $app
  python manage.py makemigrations $app
done

python manage.py migrate
python manage.py init_sys
python manage.py init_wf
python manage.py init_ticket
python manage.py init_leave
python manage.py runserver
#!/usr/bin/bash

apt-get install libpq-dev python-dev
apt install postgresql

pip install virtualenv
virtualenv -p python3 venv
source venv/bin/activate

pip install -r requirements.txt

systemctl start postgresql
python manage.py migrate

python3 manage.py runserver

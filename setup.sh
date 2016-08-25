#! /bin/bash

RED='\033[0;31m'
NC='\033[0m' # No Color

if source ./env/bin/activate; then
    echo "Virtualenv found"
else
    virtualenv -p python3 env
    source env/bin/activate
fi
pip install -r requirements.txt

setup_folder=$PWD
echo $setup_folder
# add absolute path to the wrappers

echo -e "$RED Webserver Setup started.$NC"
# WEBSERVER SETUP
cd crossval
rm db.sqlite3 

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
echo -e "$RED Set up a superuser. $NC"
python manage.py createsuperuser

#! /bin/bash

RED='\033[0;31m'
NC='\033[0m' # No Color

if source ./env/bin/activate; then
    echo -e "$RED Virtualenv Found. Using pre existing env. $NC"
else
    echo -e "$RED Virtualenv Not Found. Creating new env. $NC"
    virtualenv -p python3 env
    source env/bin/activate
fi
echo -e "$RED Installing requirements. $NC"
pip install -r requirements.txt

setup_folder=$PWD
echo -e "$RED Setup folder path is: $NC $setup_folder"
# add absolute path to the wrappers

echo -e "$RED Webserver Setup started.$NC"
# WEBSERVER SETUP
cd crossval
echo -e "$RED Removing old Database if any.$NC"
rm db.sqlite3 

echo -e "$RED Creating new database structures.$NC"
python manage.py makemigrations
echo -e "$RED Creating new database.$NC"
python manage.py migrate
echo -e "$RED Collecting static files.$NC"
python manage.py collectstatic --noinput
echo -e "$RED Set up a superuser. $NC"
python manage.py createsuperuser
echo -e "$RED Setup is done. $NC"

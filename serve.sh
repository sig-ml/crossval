#! /bin/bash

RED='\033[0;31m'
NC='\033[0m' # No Color

if source ./env/bin/activate; then
    echo -e "$RED Virtualenv Found.$NC"
    virtualenv -p python3 env
    source env/bin/activate
else
    echo -e "$RED Virtualenv Not Found. $NC Please run setup.sh or report this on github"
fi

cd crossval
python manage.py runserver
echo -e "$RED Webserver Started.$NC"

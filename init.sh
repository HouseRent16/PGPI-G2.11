#!/bin/bash
# *********************************************************************************************************************
# Script para ejecutar comandos Django en macOS y Linux
# El script asume que se encuentra en la raíz del proyecto
# Para ejecutar, primero da permisos de ejecución con 'chmod +x init.sh'
# Luego, ejecute con './init.sh'
# *********************************************************************************************************************

if [ "$1" == "--help" ]; then
    echo "Usage: ./init.sh [--notest] [--help]"
    echo "Options:"
    echo "  --help    Show this help message."
    echo "  --notest  Skip the test execution."
    echo ""
    exit 0
fi

echo "###########################################################################################################"
echo ""#                                                                                                         #""
echo "#                                                                                                         #"
echo "#                                                                                                         #"
echo "#      █████   █████                                      ███████████                        █████        #"
echo "#     ░░███   ░░███                                      ░░███░░░░░███                      ░░███         #"
echo "#      ░███    ░███   ██████  █████ ████  █████   ██████  ░███    ░███   ██████  ████████   ███████       #"
echo "#      ░███████████  ███░░███░░███ ░███  ███░░   ███░░███ ░██████████   ███░░███░░███░░███ ░░░███░        #"
echo "#      ░███░░░░░███ ░███ ░███ ░███ ░███ ░░█████ ░███████  ░███░░░░░███ ░███████  ░███ ░███   ░███         #"
echo "#      ░███    ░███ ░███ ░███ ░███ ░███  ░░░░███░███░░░   ░███    ░███ ░███░░░   ░███ ░███   ░███ ███     #"
echo "#      █████   █████░░██████  ░░████████ ██████ ░░██████  █████   █████░░██████  ████ █████  ░░█████      #"
echo "#     ░░░░░   ░░░░░  ░░░░░░    ░░░░░░░░ ░░░░░░   ░░░░░░  ░░░░░   ░░░░░  ░░░░░░  ░░░░ ░░░░░    ░░░░░       #"
echo "#                                                                                                         #"
echo "#                                                                                                         #"
echo "#                                                                                                         #"
echo "###########################################################################################################"
echo ""
echo ""

echo "========== CHECKING PYTHON VERSION =========="
echo "Checking Python version..."
python3 -c "import sys; assert sys.version_info[:2] == (3, 10), 'Incorrect Python version, requires Python 3.10'; print('Correct Python version (3.10)')"
if [ $? -ne 0 ]; then
    echo "Python version is not 3.10. Exiting..."
    exit 1
fi

echo "========== DELETING VIRTUAL ENVIRONMENT =========="
echo "Deleting virtual environment..."
rm -rf venv
echo ""

echo "========== CREATING VIRTUAL ENVIRONMENT =========="
echo "Creating virtual environment..."
python3 -m venv venv
echo ""

echo "========== ACTIVATING VIRTUAL ENVIRONMENT =========="
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

echo "========== SETTING GIT COMMIT TEMPLATE =========="
echo "Setting Git commit template..."
git config commit.template .gitmessage.txt
echo ""

echo "========== UPDATING PIP =========="
echo "Updating pip..."
python -m pip install --upgrade pip
echo ""

echo "========== INSTALLING DEPENDENCIES =========="
echo "Installing dependencies from requirements.txt..."
pip install -r ./requirements.txt
echo ""

echo "========== DELETING DATABASE =========="
echo "Deleting database..."
cd src/houseRent
rm -f db.sqlite3
echo ""

echo "========== CLEARING CACHE =========="
echo "Clearing cache..."
find . -name '__pycache__' -print -exec rm -rf {} +
echo ""

echo "========== CLEARING MIGRATIONS =========="
echo "Clearing migrations and recreating directories..."
for d in apps/*/; do
    if [ -d "${d}migrations" ]; then
        echo "Deleting migrations directory: ${d}migrations"
        rm -rf "${d}migrations"
    fi
    echo "Creating migrations directory: ${d}migrations"
    mkdir -p "${d}migrations"
    echo "Creating file: ${d}migrations/__init__.py"
    touch "${d}migrations/__init__.py"
done
echo ""

echo "========== MAKEMIGRATIONS =========="
echo "Running makemigrations..."
./manage.py makemigrations
echo ""

echo "========== MIGRATE =========="
echo "Running migrate..."
./manage.py migrate
echo ""

if [ "$1" == "--notest" ]; then
    echo "========== SKIPPING TESTS =========="
    echo "Skipping test execution because of --notest argument."
    echo ""
else
    echo "========== TEST =========="
    echo "Running tests..."
    ./manage.py test
    echo ""

    echo "========== COVERAGE REPORT =========="
    echo "Generating coverage report..."
    coverage run --source='.' manage.py test
    coverage report
    coverage html
    echo ""
fi


echo "========== LOAD DATA =========="
echo "Loading data from populate.json..."
./manage.py loaddata populate.json
echo ""

echo "========== RUN SERVER =========="
echo "Starting the server..."
./manage.py runserver
echo ""

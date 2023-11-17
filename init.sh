#!/bin/bash
# Script para ejecutar comandos Django en macOS y Linux
# El script asume que se encuentra en la raíz del proyecto
# Para ejecutar, primero da permisos de ejecución con 'chmod +x init.sh'
# Luego, ejecute con './init.sh'

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
find . -name '__pycache__' -exec rm -rf {} +
echo ""

echo "========== CLEARING MIGRATIONS =========="
echo "Clearing migrations and recreating __init__.py files..."
find . -path "*/migrations/*" -not -name "__init__.py" -delete
find . -path "*/migrations" -exec touch {}/__init__.py \;
echo ""

echo "========== MAKEMIGRATIONS =========="
echo "Running makemigrations..."
./manage.py makemigrations
echo ""

echo "========== MIGRATE =========="
echo "Running migrate..."
./manage.py migrate
echo ""

echo "========== TEST =========="
echo "Running tests..."
./manage.py test
echo ""

echo "========== LOAD DATA =========="
echo "Loading data from populate.json..."
./manage.py loaddata populate.json
echo ""

echo "========== RUN SERVER =========="
echo "Starting the server..."
./manage.py runserver
echo ""

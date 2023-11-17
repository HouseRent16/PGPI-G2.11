@echo off
REM Script para ejecutar comandos Django en Windows
REM El script asume que se encuentra en la raíz del proyecto
REM Para ejecutar, haga doble clic en este archivo o ejecute desde el símbolo del sistema './init.bat'.

echo ========== CREATING VIRTUAL ENVIRONMENT ==========
echo Creating virtual environment...
python -m venv venv
echo.

echo ========== ACTIVATING VIRTUAL ENVIRONMENT ==========
echo Activating virtual environment...
call venv\Scripts\activate
echo.

echo ========== SETTING GIT COMMIT TEMPLATE ==========
echo Setting Git commit template...
git config commit.template .gitmessage.txt
echo.

echo ========== UPDATING PIP ==========
echo Updating pip...
python -m pip install --upgrade pip
echo.

echo ========== INSTALLING DEPENDENCIES ==========
echo Installing dependencies from requirements.txt...
pip install -r ./requirements.txt
echo.

echo ========== DELETING DATABASE ==========
echo Deleting database...
cd src\houseRent
if exist "db.sqlite3" del "db.sqlite3"
echo.

echo ========== CLEARING CACHE ==========
echo Clearing cache...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo.

echo ========== CLEARING MIGRATIONS ==========
echo Clearing migrations and recreating __init__.py files...
for /d /r . %%d in (migrations) do (
    if exist "%%d" (
        del /q "%%d\*"
        echo. 2>"%%d\__init__.py"
    )
)
echo.

echo ========== MAKEMIGRATIONS ==========
echo Running makemigrations...
python manage.py makemigrations
echo.

echo ========== MIGRATE ==========
echo Running migrate...
python manage.py migrate
echo.

echo ========== TEST ==========
echo Running tests...
python manage.py test
echo.

echo ========== LOAD DATA ==========
echo Loading data from populate.json...
python manage.py loaddata populate.json
echo.

echo ========== RUN SERVER ==========
echo Starting the server...
python manage.py runserver
echo.

pause

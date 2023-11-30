@echo off
REM *********************************************************************************************************************
REM Script para ejecutar comandos Django en Windows
REM El script asume que se encuentra en la raíz del proyecto
REM Para ejecutar, haga doble clic en este archivo o ejecute desde el símbolo del sistema './init.bat'.
REM *********************************************************************************************************************

chcp 65001

SET nocheck=0
SET novenv=0
SET nodependencies=0
SET persist=0
SET notest=0

:loop
IF "%1"=="" GOTO start
IF "%1"=="--help" GOTO help
IF "%1"=="--nocheck" SET "nocheck=1" & GOTO nextarg
IF "%1"=="--novenv" SET "novenv=1" & GOTO nextarg
IF "%1"=="--nodependencies" SET "nodependencies=1" & GOTO nextarg
IF "%1"=="--persist" SET "persist=1" & GOTO nextarg
IF "%1"=="--notest" SET "notest=1" & GOTO nextarg

:nextarg
SHIFT
GOTO loop

:help
echo Usage: init.bat [--nocheck] [--novenv] [--nodependencies] [--persist] [--notest] [--help]
echo Options:
echo   --help    Show this help message.
echo   --nocheck  Skip the Python version check.
echo   --novenv  Skip the virtual environment creation.
echo   --nodependencies  Skip the dependencies installation.
echo   --persist  Persist the database.
echo   --notest  Skip the test execution.
exit /b

:start

echo ###########################################################################################################
echo #                                                                                                         #
echo #                                                                                                         #
echo #                                                                                                         #
echo #      █████   █████                                      ███████████                        █████        #
echo #     ░░███   ░░███                                      ░░███░░░░░███                      ░░███         #
echo #      ░███    ░███   ██████  █████ ████  █████   ██████  ░███    ░███   ██████  ████████   ███████       #
echo #      ░███████████  ███░░███░░███ ░███  ███░░   ███░░███ ░██████████   ███░░███░░███░░███ ░░░███░        #
echo #      ░███░░░░░███ ░███ ░███ ░███ ░███ ░░█████ ░███████  ░███░░░░░███ ░███████  ░███ ░███   ░███         #
echo #      ░███    ░███ ░███ ░███ ░███ ░███  ░░░░███░███░░░   ░███    ░███ ░███░░░   ░███ ░███   ░███ ███     #
echo #      █████   █████░░██████  ░░████████ ██████ ░░██████  █████   █████░░██████  ████ █████  ░░█████      #
echo #     ░░░░░   ░░░░░  ░░░░░░    ░░░░░░░░ ░░░░░░   ░░░░░░  ░░░░░   ░░░░░  ░░░░░░  ░░░░ ░░░░░    ░░░░░       #
echo #                                                                                                         #
echo #                                                                                                         #
echo #                                                                                                         #
echo ###########################################################################################################
echo.
echo.

IF "%nocheck%"=="1" (
    echo ========== SKIPPING PYTHON VERSION CHECK ==========
    echo Skipping Python version check because of --nocheck argument.
    echo.
) ELSE (
    echo ========== CHECKING PYTHON VERSION ==========
    echo Checking Python version...
    python -c "import sys; sys.exit(0 if sys.version_info[:2] == (3, 10) else 1)"
    if %errorlevel% neq 0 (
        echo Python version is not 3.10. Exiting...
        exit /b
    )
    echo.
)

IF "%novenv%"=="1" (
    echo ========== SKIPPING VENV ==========
    echo Skipping virtual environment creation because of --novenv argument.
    echo.
) ELSE (
    echo ========== DELETING VIRTUAL ENVIRONMENT ==========
    echo Deleting virtual environment...
    if exist "venv" rmdir /s /q "venv"
    echo.

    echo ========== CREATING VIRTUAL ENVIRONMENT ==========
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

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

IF "%nodependencies%"=="1" (
    echo ========== SKIPPING DEPENDENCIES INSTALLATION ==========
    echo Skipping dependencies installation because of --nodependencies argument.
    echo.
) ELSE (
    echo ========== INSTALLING DEPENDENCIES ==========
    echo Installing dependencies from requirements.txt...
    pip install -r ./requirements.txt
    echo.
)

cd src\houseRent

IF "%persist%"=="1" (
    echo ========== PERSISTING DATABASE ==========
    echo Persisting database because of --persist argument.
    echo.
) ELSE (
    echo ========== DELETING DATABASE ==========
    echo Deleting database...
    if exist "db.sqlite3" del "db.sqlite3"
    echo.
)

echo ========== CLEARING CACHE ==========
echo Clearing cache...
for /d /r . %%d in (__pycache__) do (
    if exist "%%d" (
        echo Deleting cache directory: %%d
        rd /s /q "%%d"
    )
)
echo.

echo ========== CLEARING MIGRATIONS ==========
echo Clearing migrations and recreating directories...
for /d %%d in (apps\*) do (
    if exist "%%d\migrations" (
        echo Deleting migrations directory: %%d\migrations
        rd /s /q "%%d\migrations"
    )
    echo Creating migrations directory: %%d\migrations
    mkdir "%%d\migrations"
    echo Creating file: %%d\migrations\__init__.py
    echo. 2>"%%d\migrations\__init__.py"
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

IF "%notest%"=="1" (
    echo ========== SKIPPING TESTS ==========
    echo Skipping test execution because of --notest argument.
    echo.
) ELSE (
    echo ========== TEST ==========
    echo Running tests...
    python manage.py test
    echo.

    echo ========== COVERAGE REPORT ==========
    echo Generating coverage report...
    coverage run --source='.' manage.py test
    coverage report
    coverage html
    echo.
)

echo ========== LOAD DATA ==========
echo Loading data from populate.json...
python manage.py loaddata populate.json
echo.

echo ========== RUN SERVER ==========
echo Starting the server...
python manage.py runserver
echo.

pause

@ECHO OFF
REM Oracle Forms to XML Converter - Launcher Script
REM Quick start script for Windows

ECHO ========================================
ECHO Oracle Forms to XML Converter
ECHO ========================================
ECHO.

REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO ERROR: Python no esta instalado o no esta en el PATH
    ECHO Por favor, instala Python 3.8 o superior desde https://www.python.org
    PAUSE
    EXIT /B 1
)

ECHO Iniciando aplicacion...
ECHO.

REM Change to the src directory and run the application
cd oracle_forms_converter\src
python main.py

IF %ERRORLEVEL% NEQ 0 (
    ECHO.
    ECHO ERROR: La aplicacion termino con errores
    PAUSE
)

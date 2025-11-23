#!/bin/bash
# Oracle Forms to XML Converter - Launcher Script
# Quick start script for Linux/Mac

echo "========================================"
echo "Oracle Forms to XML Converter"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 no esta instalado"
    echo "Por favor, instala Python 3.8 o superior"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

# Check if tkinter is available
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo ""
    echo "WARNING: tkinter no esta instalado"
    echo "Instala con: sudo apt-get install python3-tk (Ubuntu/Debian)"
    echo ""
    exit 1
fi

echo "Iniciando aplicacion..."
echo ""

# Change to the src directory and run the application
cd oracle_forms_converter/src
python3 main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: La aplicacion termino con errores"
    read -p "Presiona Enter para continuar..."
fi

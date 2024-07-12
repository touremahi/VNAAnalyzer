#!/bin/bash
set -e

# Set the Python executable path and the main script path
PYTHON_EXE=python3
MAIN_SCRIPT=vna_analyzer/main.py

# Create the executable using Nuitka
$PYTHON_EXE -m nuitka --standalone --onefile --plugin-enable=pyside6 --include-data-file=vna_analyzer/resources/styles.qss=vna_analyzer/resources/styles.qss --output-dir=dist $MAIN_SCRIPT

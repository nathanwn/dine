#!/bin/bash

# Run this file to setup your development environment
# Change the following variable to set the virtual environment location
PYTHON_EXEC="python3.10"
VENV_DIR=".venv"

# Create virtual environment
$PYTHON_EXEC -m venv $VENV_DIR

# Activate virtual environment
source ./$VENV_DIR/bin/activate

# Ensure the newest version of pip
pip3 install --upgrade pip

# Install packages, including dev dependencies
pip3 install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

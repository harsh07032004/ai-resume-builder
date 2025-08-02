#!/bin/bash

# Activate virtual environment and run Flask app
cd "$(dirname "$0")"
source venv/bin/activate
export FLASK_APP=app.py
export FLASK_ENV=development
python app.py
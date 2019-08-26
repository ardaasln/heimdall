#!/usr/bin/env bash

python3 -m venv venv
. venv/bin/activate
export FLASK_APP=app.py
export FLASK_ENV=development
pip install -e .
flask run
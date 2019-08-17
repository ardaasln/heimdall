#!/usr/bin/env bash

export LC_ALL=en_US.utf-8
export LANG=en_US.utf-8
python3 -m venv venv
. venv/bin/activate
export FLASK_APP=app.py
pip install -e .
flask run --host=0.0.0.0 > /dev/null 2>&1
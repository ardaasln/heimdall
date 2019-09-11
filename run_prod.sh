#!/usr/bin/env bash

export LC_ALL=en_US.utf-8
export LANG=en_US.utf-8
python3 -m venv venv
. venv/bin/activate
export FLASK_APP=app.py
export FLASK_ENV=production
pip install -e .
gunicorn -w 4 --bind 0.0.0.0 --log-level=info --log-file=/tmp/heimdall.log app:app
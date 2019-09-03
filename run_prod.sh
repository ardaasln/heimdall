#!/usr/bin/env bash

export LC_ALL=en_US.utf-8
export LANG=en_US.utf-8
python3 -m venv venv
. venv/bin/activate
export FLASK_APP=app.py
export FLASK_ENV=production
pip install -e .
flask run --host=0.0.0.0 > /tmp/heimdall.log 2>&1
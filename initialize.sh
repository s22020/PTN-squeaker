#!/bin/sh

export FLASK_APP=app.py

flask db init
flask db migrate
flask db upgrade
flask db stamp
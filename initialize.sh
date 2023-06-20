#!/bin/sh

export FLASK_APP=app.py

export MAIL_USERNAME='changeit'
export MAIL_PASSWORD='changeit'
export SQUEAKER_MAIL_SENDER='changeit'
export SQUEAKER_MAIL_SUBJECT_PREFIX='changeit'

flask db init
flask db migrate
flask db upgrade
flask db stamp
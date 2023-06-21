#!/bin/sh

export FLASK_APP=app.py
export FLASK_CONFIG='dev'


export MAIL_USERNAME='changeit'
export MAIL_PASSWORD='changeit'

flask db init
flask db migrate
flask db upgrade
flask db stamp
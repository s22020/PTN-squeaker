#!/bin/sh

flask db migrate
flask db upgrade
flask db stamp
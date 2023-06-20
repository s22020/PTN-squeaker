from flask import render_template
from . import main


@main.app_errorhandler(404)
def not_found(e):
    return render_template('not_found.html'), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
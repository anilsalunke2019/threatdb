# -*- coding: utf-8 -*-
"""
A manage.py script to centralized all cli commands
Created on 21/10/2019
@author: Anurag
"""

# imports
from api.views import app as application
from api.models import db


def create_app():
    """
    Creates flask app instance
    :return:
    """
    db.init_app(application)
    return application


app = create_app()


def migrate():
    """
    A migrate command for creating database tables
    :return:
    """
    with app.app_context():
        db.init_app(app)
        db.create_all()


def runserver():
    """
    For running flask server
    :return:
    """
    app.run(host='0.0.0.0', port="80")


if __name__ == '__main__':
    runserver()

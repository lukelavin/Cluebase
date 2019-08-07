# services/users/manage.py


import sys
import unittest

from flask.cli import FlaskGroup

from app import create_app, db

app = create_app()
cli = FlaskGroup(create_app=create_app)

if __name__ == '__main__':
    cli()

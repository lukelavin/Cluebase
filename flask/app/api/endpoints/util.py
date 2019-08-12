from datetime import timedelta, datetime
from flask import Blueprint, request, redirect
from flask_restful import Resource, Api
from sqlalchemy import exc

from app import db, cache
from app.api.models import Seasons

start_time = datetime.now()

util_blueprint = Blueprint('util', __name__)
api = Api(util_blueprint)


class Uptime(Resource):
    def get(self):
        return {
            'status': 'success',
            'uptime': str(datetime.now() - start_time)
        }


@util_blueprint.route('/')
@util_blueprint.route('/docs')
def docs():
    return redirect('https://cluebase.readthedocs.io', code=302)

api.add_resource(Uptime, '/uptime')

from datetime import timedelta, datetime
from flask import Blueprint, request
from flask_restful import Resource, Api
from sqlalchemy import exc

from app import db, cache
from app.api.models import Seasons

start_time = datetime.now()

util_blueprint = Blueprint('util', __name__)
api = Api(util_blueprint)

class Index(Resource):
    def get(self):
        return "Hello world!"


class Uptime(Resource):
    @cache.cached(timeout=5)
    def get(self):
        return {
            'uptime': str(datetime.now() - start_time)
        }


api.add_resource(Index, '/')
api.add_resource(Uptime, '/uptime')

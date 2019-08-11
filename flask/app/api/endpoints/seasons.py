from flask import Blueprint, request
from flask_restful import Resource, Api
from sqlalchemy import exc

from app import db, cache
from app.api.models import Seasons

seasons_blueprint = Blueprint('seasons', __name__)
api = Api(seasons_blueprint)

class SeasonsList(Resource):
    @cache.cached()
    def get(self):
        try:
            result = [season.to_json() for season in Seasons.query.all()]
        except Exception as e:
            return {
                'status' : 'failure',
                'error': repr(e)
            }


api.add_resource(SeasonsList, '/seasons')

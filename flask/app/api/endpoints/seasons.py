from flask import Blueprint, request
from flask_restful import Resource, Api
from sqlalchemy import exc

from app import db, cache
from app.api.models import Seasons
from app.api.exceptions import IdNotFoundError

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
            }, 400

        return {
            'status': 'success',
            'data': result
        }

class SeasonById(Resource):
    @cache.memoize()
    def get(self, id):
        try:
            result = [season.to_json() for season in Seasons.query.filter_by(id=id).all()]

            if len(result) > 0:
                return {
                    'status' : 'success',
                    'data' : result
                }, 200
            else:
                raise IdNotFoundError(f'Season with id {id} could not be found.')
        except Exception as e:
            return {
                'status' : 'failure',
                'error': repr(e)
            }, 404


api.add_resource(SeasonsList, '/seasons')
api.add_resource(SeasonById, '/seasons/<int:id>')

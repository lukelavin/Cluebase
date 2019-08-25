from flask import Blueprint, request
from flask_restful import Resource, Api

from app import db, cache
from app.api.models import Games

games_blueprint = Blueprint('games', __name__)
api = Api(games_blueprint)

class GamesList(Resource):
    def get(self):
        try:
            result = [game.to_json() for game in Games.query
                                                    .order_by(Games.id)
                                                    .limit(50)
                                                    .all()]
        except Exception as e:
            return {
                'status' : 'failure',
                'error' : repr(e)
            }, 400
        return result


class GameById(Resource):
    def get(self, id):
        try:
            result = [game.to_json() for game in Games.query
                                                    .filter_by(id=id)
                                                    .all()]
            if len(result) < 1:
                raise IdNotFoundError(f'Game with id {id} does not exist')
        except Exception as e:
            return {
                'status': 'failure',
                'error': repr(e)
            }, 400

        return {
            'status': 'success',
            'data': result
        }


api.add_resource(GamesList, '/games')

from flask import Blueprint, request
from flask_restful import Resource, Api

from app import db, cache
from app.api.models import Clues

clues_blueprint = Blueprint('clues', __name__)
api = Api(clues_blueprint)

class CluesList(Resource):
    def get(self):
        try:
            result = [clue.to_json() for clue in Clues.query
                                                    .order_by(Clues.id)
                                                    .limit(50)
                                                    .all()]
        except Exception as e:
            return {
                'status' : 'failure',
                'error' : repr(e)
            }, 400
        return result


api.add_resource(CluesList, '/clues')

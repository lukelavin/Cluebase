from flask import Blueprint, request
from flask_restful import Resource, Api
from sqlalchemy import exc

from app import db
from app.api.models import Seasons

resources_blueprint = Blueprint('resources', __name__)
api = Api(resources_blueprint)

class SeasonsList(Resource):
    def get(self):
        return [season.to_json() for season in Seasons.query.all()]


api.add_resource(SeasonsList, '/seasons')

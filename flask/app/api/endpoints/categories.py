from flask import Blueprint, request
from flask_restful import Resource, Api
from sqlalchemy import func

from app import db, cache
from app.api.models import Clues

categories_blueprint = Blueprint('categories', __name__)
api = Api(categories_blueprint)

def category_to_json(category):
    return {
        'category': category[0],
        'question_count': category[1]
    }

@cache.memoize()
def get_categories():
    return [category_to_json(category) for category in (Clues.query
                .with_entities(Clues.category,
                                func.count(Clues.category))
                .group_by(Clues.category)
                .order_by(func.count(Clues.category).desc())
                .limit(50)
                .all())]

class CategoriesList(Resource):
    def get(self):
        try:
            result = get_categories()
        except Exception as e:
            return {
                'status' : 'failure',
                'error' : repr(e)
            }, 400
        return {
            'status' : 'success',
            'data' : result
        }


api.add_resource(CategoriesList, '/categories')

from flask import Blueprint, request
from flask_restful import Resource, Api
from sqlalchemy import func

from app import db, cache
from app.api.models import Clues
from app.api.exceptions import LimitNotANumberError, LimitOverMaxError, \
                                OffsetNotANumberError

categories_blueprint = Blueprint('categories', __name__)
api = Api(categories_blueprint)

def category_to_json(category):
    return {
        'category': category[0],
        'clue_count': category[1]
    }

@cache.memoize()
def get_categories(limit, offset):
    digits = '0123456789'
    for c in str(limit):
        if digits.find(c) == -1:
            raise LimitNotANumberError('"Limit" query parameter is not a valid number')
    if int(limit) > 2000:
        raise LimitOverMaxError('Requested too many resources. Maximum "limit" is 2000')
    for c in str(offset):
        if digits.find(c) == -1:
            raise OffsetNotANumberError('"offset" query parameter is not a valid number')

    return [category_to_json(category) for category in (Clues.query
                .with_entities(Clues.category,
                                func.count(Clues.category))
                .group_by(Clues.category)
                .order_by(func.count(Clues.category).desc())
                .limit(limit)
                .offset(offset)
                .all())]

class CategoriesList(Resource):
    def get(self):
        limit = request.args.get('limit', 50)
        offset = request.args.get('offset', 0)

        try:
            result = get_categories(limit, offset)
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

import random

from flask import Blueprint, request
from flask_restful import Resource, Api
from sqlalchemy import func

from app import db, cache
from app.api.models import Clues
from app.api.exceptions import LimitNotANumberError, LimitOverMaxError, \
                               OffsetNotANumberError, OrderByInvalidError, \
                               SortInvalidError, IdNotFoundError

clues_blueprint = Blueprint('clues', __name__)
api = Api(clues_blueprint)


@cache.memoize()
def get_clues(limit, offset, order_by, sort):
    string_to_col = {
        'id' : Clues.id,
        'game_id' : Clues.game_id,
        'value' : Clues.value,
        'daily_double' : Clues.daily_double,
        'round' : Clues.round,
        'category' : Clues.category,
        'clue' : Clues.clue,
        'response' : Clues.response
    }

    ####
    # Checking for exceptions
    ####

    digits = '0123456789'
    for c in str(limit):
        if digits.find(c) == -1:
            raise LimitNotANumberError('"Limit" query parameter is not a valid number')
    if int(limit) > 2000:
        raise LimitOverMaxError('Requested too many resources. Maximum "limit" is 1000')
    for c in str(offset):
        if digits.find(c) == -1:
            raise OffsetNotANumberError('"offset" query parameter is not a valid number')
    if string_to_col.get(order_by, 'none') == 'none':
        raise OrderByInvalidError('"order_by" query parameter is invalid')
    if sort != 'asc' and sort != 'desc':
        raise SortInvalidError('"sort" query parameter must be "asc" or "desc"')

    if sort == 'asc':
        return [clue.to_json() for clue in Clues.query
        .order_by(string_to_col[order_by])
        .limit(limit)
        .offset(offset)
        .all()]
    if sort == 'desc':
        return [clue.to_json() for clue in Clues.query
        .order_by(string_to_col[order_by].desc())
        .limit(limit)
        .offset(offset)
        .all()]

# TODO: order by more than one column
# TODO: search category and/or value
class CluesList(Resource):
    def get(self):
        limit = request.args.get('limit', 50)
        offset = request.args.get('offset', 0)
        order_by = request.args.get('order_by', 'id')
        sort = request.args.get('sort', 'asc')
        try:
            result = get_clues(limit, offset, order_by, sort)
        except Exception as e:
            return {
                'status' : 'failure',
                'error': repr(e)
            }, 400

        return {
            'status' : 'success',
            'data': result
        }, 200


@cache.memoize()
def get_clue_by_id(id):
    result = [clue.to_json() for clue in Clues.query.filter_by(id=id).all()]

    if len(result) > 0:
        return result
    else:
        raise IdNotFoundError(f'Clue with id {id} could not be found.')


class ClueById(Resource):
    def get(self, id):
        try:
            result = get_clue_by_id(id)
        except Exception as e:
            return {
                'status' : 'failure',
                'error': repr(e)
            }, 404

        return {
            'status' : 'success',
            'data': result
        }, 200


def get_clue_random(limit):
    digits = '0123456789'
    for c in str(limit):
        if digits.find(c) == -1:
            raise LimitNotANumberError('"Limit" query parameter is not a valid number')
    if int(limit) > 100:
        raise LimitOverMaxError('Requested too many resources. Maximum "limit" is 100')

    results = []
    max = Clues.query.with_entities(func.max(Clues.id)).first()[0]
    usedIds = [0]

    randId = 0
    randResult = []

    while len(results) < int(limit):
        while len(randResult) < 1 or randId in usedIds:
            randId = random.randint(1, max)
            randResult = [clue.to_json() for clue in Clues.query
                        .filter_by(id = randId)
                        .all()]
        results.append(randResult[0])
        usedIds.append(randId)

    return results

class CluesRandom(Resource):
    def get(self):
        limit = request.args.get('limit', 1)

        try:
            result = get_clue_random(limit)
        except Exception as e:
            return {
                'status' : 'failure',
                'error': repr(e)
            }, 400

        return {
            'status' : 'success',
            'data': result
        }, 200

api.add_resource(CluesList, '/clues')
api.add_resource(ClueById, '/clues/<int:id>')
api.add_resource(CluesRandom, '/clues/random')

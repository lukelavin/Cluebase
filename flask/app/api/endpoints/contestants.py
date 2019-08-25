import random

from flask import Blueprint, request
from flask_restful import Resource, Api
from sqlalchemy import func

from app import db, cache
from app.api.models import Contestants
from app.api.exceptions import LimitNotANumberError, LimitOverMaxError, \
                               OffsetNotANumberError, OrderByInvalidError, \
                               SortInvalidError, IdNotFoundError, \
                               NameNotFoundError

contestants_blueprint = Blueprint('contestants', __name__)
api = Api(contestants_blueprint)

@cache.memoize()
def get_contestants(limit, offset, order_by, sort):
    string_to_col = {
        'id' : Contestants.id,
        'name' : Contestants.name,
        'notes' : Contestants.notes,
        'games_played' : Contestants.games_played,
        'total_winnings' : Contestants.total_winnings
    }

    ####
    # Checking for exceptions
    ####

    digits = '0123456789'
    for c in str(limit):
        if digits.find(c) == -1:
            raise LimitNotANumberError('"Limit" query parameter is not a valid number')
    if int(limit) > 2000:
        raise LimitOverMaxError('Requested too many resources. Maximum "limit" is 2000')
    for c in str(offset):
        if digits.find(c) == -1:
            raise OffsetNotANumberError('"offset" query parameter is not a valid number')
    if string_to_col.get(order_by, 'none') == 'none':
        raise OrderByInvalidError('"order_by" query parameter is invalid')
    if sort != 'asc' and sort != 'desc':
        raise SortInvalidError('"sort" query parameter must be "asc" or "desc"')

    if sort == 'asc':
        return [contestant.to_json() for contestant in Contestants.query
        .order_by(string_to_col[order_by])
        .limit(limit)
        .offset(offset)
        .all()]
    if sort == 'desc':
        return [contestant.to_json() for contestant in Contestants.query
        .order_by(string_to_col[order_by].desc())
        .limit(limit)
        .offset(offset)
        .all()]

# TODO: order by more than one column
# TODO: search name or notes
class ContestantsList(Resource):
    def get(self):
        limit = request.args.get('limit', 50)
        offset = request.args.get('offset', 0)
        order_by = request.args.get('order_by', 'id')
        sort = request.args.get('sort', 'asc')
        try:
            result = get_contestants(limit, offset, order_by, sort)
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
def get_contestant_by_id(id):
    result = [contestant.to_json() for contestant in Contestants.query
                                                    .filter_by(id=id)
                                                    .all()]

    if len(result) < 1:
        raise IdNotFoundError('Contestant id not found in database.')

    return result


class ContestantById(Resource):
    def get(self, id):
        try:
            result = get_contestant_by_id(id)
        except Exception as e:
            return {
                'status': 'failure',
                'error': repr(e)
            }, 404

        return {
            'status': 'success',
            'data': result
        }, 200


@cache.memoize()
def get_contestant_by_name(name):
    result = [contestant.to_json() for contestant in Contestants.query
                        .filter(func.lower(Contestants.name) == name)
                        .all()]

    if len(result) < 1:
        raise NameNotFoundError(f'Contestant with name {name} name not found in database. ' + \
                                'Make sure to use underscores as spaces.')

    return result

def get_contestant_random(limit):
    digits = '0123456789'
    for c in str(limit):
        if digits.find(c) == -1:
            raise LimitNotANumberError('"Limit" query parameter is not a valid number')
    if int(limit) > 100:
        raise LimitOverMaxError('Requested too many resources. Maximum "limit" is 100')

    results = []
    max = Contestants.query.with_entities(func.max(Contestants.id)).first()[0]
    usedIds = [0]

    randId = 0
    randResult = []

    while len(results) < int(limit):
        while len(randResult) < 1 or randId in usedIds:
            randId = random.randint(1, max)
            randResult = [contestant.to_json() for contestant in Contestants.query
                        .filter_by(id = randId)
                        .all()]
        results.append(randResult[0])
        usedIds.append(randId)

    return results


class ContestantByName(Resource):
    def get(self, name):
        if name == 'random':
            limit = request.args.get('limit', 1)
            try:
                result = get_contestant_random(limit)
            except Exception as e:
                return {
                    'status': 'failure',
                    'error': repr(e)
                }, 400
        else:
            name = name.replace('_', ' ').replace('-', ' ')

            try:
                result = get_contestant_by_name(name)
            except Exception as e:
                return {
                    'status': 'failure',
                    'error': repr(e)
                }, 404

        return {
            'status': 'success',
            'data': result
        }, 200

api.add_resource(ContestantsList, '/contestants')
api.add_resource(ContestantById, '/contestants/<int:id>')
api.add_resource(ContestantByName, '/contestants/<string:name>')

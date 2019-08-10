from flask import Blueprint, request
from flask_restful import Resource, Api

from app import db, cache
from app.api.models import Contestants
from app.api.exceptions import LimitNotANumberError, LimitOverMaxError, \
                               OffsetNotANumberError, OrderByInvalidError, \
                               SortInvalidError

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
    if int(limit) > 5000:
        raise LimitOverMaxError('Requested too many resources. Maximum "limit" is 5000')
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
            'contestants': result
        }, 200


api.add_resource(ContestantsList, '/contestants')

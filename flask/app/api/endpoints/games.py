from flask import Blueprint, request
from flask_restful import Resource, Api

from app import db, cache
from app.api.models import Games
from app.api.exceptions import LimitNotANumberError, LimitOverMaxError, \
                               OffsetNotANumberError, OrderByInvalidError, \
                               SortInvalidError, IdNotFoundError, \
                               NameNotFoundError

games_blueprint = Blueprint('games', __name__)
api = Api(games_blueprint)

@cache.memoize()
def get_games(limit, offset, order_by, sort):
    string_to_col = {
        'id' : Games.id,
        'episode_num' : Games.episode_num,
        'season_id' : Games.season_id,
        'air_date' : Games.air_date,
        'notes' : Games.notes,
        'contestant1' : Games.contestant1,
        'contestant2' : Games.contestant2,
        'contestant3' : Games.contestant3,
        'winner' : Games.winner,
        'score1' : Games.score1,
        'score2' : Games.score2,
        'score3' : Games.score3,
    }

    ####
    # Checking for exceptions
    ####

    digits = '0123456789'
    for c in str(limit):
        if digits.find(c) == -1:
            raise LimitNotANumberError('"Limit" query parameter is not a valid number')
    if int(limit) > 1000:
        raise LimitOverMaxError('Requested too many resources. Maximum "limit" is 1000')
    for c in str(offset):
        if digits.find(c) == -1:
            raise OffsetNotANumberError('"offset" query parameter is not a valid number')
    if string_to_col.get(order_by, 'none') == 'none':
        raise OrderByInvalidError('"order_by" query parameter is invalid')
    if sort != 'asc' and sort != 'desc':
        raise SortInvalidError('"sort" query parameter must be "asc" or "desc"')

    if sort == 'asc':
        return [game.to_json() for game in Games.query
        .order_by(string_to_col[order_by])
        .limit(limit)
        .offset(offset)
        .all()]
    if sort == 'desc':
        return [game.to_json() for game in Games.query
        .order_by(string_to_col[order_by].desc())
        .limit(limit)
        .offset(offset)
        .all()]

class GamesList(Resource):
    def get(self):
        limit = request.args.get('limit', 50)
        offset = request.args.get('offset', 0)
        order_by = request.args.get('order_by', 'id')
        sort = request.args.get('sort', 'asc')

        try:
            result = get_games(limit, offset, order_by, sort)
        except Exception as e:
            return {
                'status' : 'failure',
                'error' : repr(e)
            }, 400
        return {
            'status': 'success',
            'data': result
        }

# TODO: 'since' filter
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
api.add_resource(GameById, '/games/<int:id>')

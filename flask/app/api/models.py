from flask_sqlalchemy import SQLAlchemy

from app import db

class Seasons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season_name = db.Column(db.String(16))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    total_games = db.Column(db.Integer)

    def __repr__(self):
        return f'Season [id = {self.id}, season_name = {self.season_name}' + \
                f', start_date = {self.start_date}, end_date = {self.end_date}' + \
                f', total_games = {self.total_games}]'

    def to_json(self):
        return {
            'id': self.id,
            'season_name': self.season_name,
            'start_date': str(self.start_date),
            'end_date': str(self.end_date),
            'total_games': self.total_games
        }


class Contestants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    notes = db.Column(db.String())
    games_played = db.Column(db.Integer, nullable=False)
    total_winnings = db.Column(db.Integer)

    def __repr__(self):
        return f'Contestant [id = {self.id}, name = {self.name}, ' + \
                f'notes = {self.notes}, games_played = {self.games_played}, ' + \
                f'total_winnings = {self.total_winnings}]'

    def to_json(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'notes' : self.notes,
            'games_played' : self.games_played,
            'total_winnings' : self.total_winnings
        }


class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    episode_num = db.Column(db.Integer, unique=True)
    season_id = db.Column(db.Integer, db.ForeignKey('seasons.id'))
    air_date = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.String())
    contestant1 = db.Column(db.Integer, db.ForeignKey('contestants.id'))
    contestant2 = db.Column(db.Integer, db.ForeignKey('contestants.id'))
    contestant3 = db.Column(db.Integer, db.ForeignKey('contestants.id'))
    winner = db.Column(db.Integer, db.ForeignKey('contestants.id'))
    score1 = db.Column(db.Integer)
    score2 = db.Column(db.Integer)
    score3 = db.Column(db.Integer)

    def __repr__(self):
        return f'Game [id = {self.id}, episode_num = {episode_num}, ' + \
                f'season_id = {season_id}, air_date = {air_date}, notes = {notes}, ' + \
                f'contestant1 = {contestant1}, contestant2 = {contestant2}, ' + \
                f'contestant3 = {contestant3}, winner = {winner}, score1 = {score1}, ' + \
                f'score2 = {score2}, score3 = {score3}]'

    def to_json(self):
        return {
            'id' : self.id,
            'episode_num' : self.episode_num,
            'season_id' : self.season_id,
            'air_date' : str(self.air_date),
            'notes' : self.notes,
            'contestant1': self.contestant1,
            'contestant2': self.contestant2,
            'contestant3' : self.contestant3,
            'winner' : self.winner,
            'score1' : self.score1,
            'score2' : self.score2,
            'score3' : self.score3
        }


class Clues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    value = db.Column(db.Integer, nullable=False)
    daily_double = db.Column(db.Boolean, nullable=False)
    round = db.Column(db.String(), nullable=False)
    category = db.Column(db.String(), nullable=False)
    clue = db.Column(db.String(), nullable=False)
    response = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'Clue [id = {self.id}, game_id = {self.game_id}, ' + \
                f'value = {self.value}, daily_double = {self.daily_double, }' + \
                f'round = {self.round}, category = {self.category}, ' + \
                f'clue = {self.clue}, response = {self.response}]'

    def to_json(self):
        return {
            'id' : self.id,
            'game_id' : self.game_id,
            'value' : self.value,
            'daily_double' : self.daily_double,
            'round' : self.round,
            'category' : self.category,
            'clue' : self.clue,
            'response' : self.response
        }

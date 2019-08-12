# services/users/project/__init.py

import os
from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache


# instantiate the db
db = SQLAlchemy()
cache = Cache()


# create the app (app factory pattern)
def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    cache.init_app(app)

    # register blueprints
    from app.api.endpoints.util import util_blueprint
    app.register_blueprint(util_blueprint)
    from app.api.endpoints.seasons import seasons_blueprint
    app.register_blueprint(seasons_blueprint)
    from app.api.endpoints.contestants import contestants_blueprint
    app.register_blueprint(contestants_blueprint)
    from app.api.endpoints.games import games_blueprint
    app.register_blueprint(games_blueprint)
    from app.api.endpoints.clues import clues_blueprint
    app.register_blueprint(clues_blueprint)
    from app.api.endpoints.categories import categories_blueprint
    app.register_blueprint(categories_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app

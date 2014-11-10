from flask import Flask
from flask.ext.bootstrap import Bootstrap
from config import config
import os

bootstrap = Bootstrap()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)

    from app.main import main as mainBlueprint
    app.register_blueprint(mainBlueprint)

    return app

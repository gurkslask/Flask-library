from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from config import config

bootstrap = Bootstrap()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_objection(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)

    from main import main as mainBlueprint
    app.register_blueprint(mainBlueprint)

    return app

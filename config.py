import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SecretKey = os.environ.get('SecretKey') or 'NKDBDKFBAD/&%¤56563hblfds'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    Debug = True


class TestingConfig(Config):
    Testing = True


class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

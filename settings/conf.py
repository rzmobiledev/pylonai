class Config(object):
    DATABASE = 'tester.sqlite'


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    DEBUG = False

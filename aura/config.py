
class Config(object):
    DEBUG = False
    TESTING = False

    import os
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Log file (the directory must exist)
    APPLICATION_LOG = os.path.join(BASE_DIR, 'log', 'application.log')
    ACCESS_LOG = os.path.join(BASE_DIR, 'log', 'access.log')
    BEETS_CONFIG = '/home/gabeos/.config/beets/library.db'

class ProductionConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True

class TestConfig(Config):
    DEBUG = True
    TESTING = True

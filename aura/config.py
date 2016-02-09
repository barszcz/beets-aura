
class Config(object):
    DEBUG = False
    TESTING = False

    import os
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Log file (the directory must exist)
    APPLICATION_LOG = os.path.join(BASE_DIR, 'log', 'application.log')
    ACCESS_LOG = os.path.join(BASE_DIR, 'log', 'access.log')

    EXTRA_MIMETYPES = {
        'audio/flac': '.flac'
    }

class ProductionConfig(Config):
    pass

class DevConfig(Config):
    LIBRARY_DB_PATH = "/home/gabeos/.config/beets/library.db"
    MUSIC_DIR = "/home/gabeos/music_library"
    DEBUG = True

class TestConfig(Config):
    LIBRARY_DB_PATH = "/home/gabeos/projects/aura/test/rsrc/config/library.db"
    MUSIC_DIR = "/home/gabeos/projects/aura/test/rsrc/music"
    DEBUG = True
    TESTING = True


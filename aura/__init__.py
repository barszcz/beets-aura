
from .aura import aura
from .config import DevConfig, ProductionConfig, TestConfig
import mimetypes

def add_mimetypes(app):
    app.config['MIMETYPES'] = mimetypes
    if 'EXTRA_MIMETYPES' in app.config:
        for tpe, ext in app.config['EXTRA_MIMETYPES']:
            app.config['MIMETYPES'].add_type(tpe,ext)

def configure_aura(config_env='dev'):
    config = DevConfig
    if config_env == 'production':
        config = ProductionConfig
    elif config_env == 'test':
        config = TestConfig

    aura.config.from_object(config)
    return aura

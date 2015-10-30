
from .aura import aura
from .config import Dev, Production

def make_aura(beetslib, config='dev'):
    config = Dev
    if 'config' == 'production':
        config = Production

    aura.config.from_object(config)
    aura.config.BEETS_LIB = beetslib
    return aura


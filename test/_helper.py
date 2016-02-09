

import os, random, mimetypes

from contextlib import contextmanager
from flask import appcontext_pushed, g
import unittest
from beets.library import Library, Item

from aura import configure_aura

def get_rel_path(path_component):
    return os.path.join(os.path.dirname(__file__),path_component)

def get_lib():
    return Library(get_rel_path('rsrc/config/library.db'),
                   get_rel_path('rsrc/music'))

@contextmanager
def beets_library(app):
    def handler(sender, **kwargs):
        g.lib = Library('rsrc/config/library.db', './rsrc/music')
    with appcontext_pushed.connected_to(handler, app):
        yield

class URLHelper(object):
    prefix = '/aura/v0.1'
    def aura_url(self,rel_url):
        if rel_url.startswith('/'):
            return self.prefix + rel_url
        return self.prefix + '/' + rel_url

    def audio_url(self,track_id):
        return self.aura_url('tracks/{}/audio'.format(track_id))

    def request_audio(self, item_id, headers=[]):
        url = self.audio_url(item_id)
        return self.client.get(url, headers=headers)

class AuraTestCase(unittest.TestCase, URLHelper):

    def setUp(self):
        self.app = configure_aura(config_env='test')
        self.client = self.app.test_client()
        self.lib = get_lib()

    def item_mime(self,item):
        return mimetypes.guess_type(item.path)[0]

    def item_filesize(self,item):
        return item.try_filesize()

    def item_query(self, query=u""):
        return self.lib._fetch(Item,query)

    def random_item(self,query=u""):
        return random.choice(self.item_query(query))

    def random_item_id(self,query=u""):
        return self.random_item(query).id

    def items_all_formats(self):
        return map(lambda fmt: self.random_item(u"format:{}".format(fmt)),
                   set(map(lambda i: i.format, self.item_query())))


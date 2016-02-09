#!/usr/bin/env python

from flask import Flask, g
from flask_restful import Api
from flask_restful.utils import cors

from beets.library import Library
from .models import Aura, Stats
from .models import Track, TrackList, TrackAudio
from .models import Album, AlbumList
from .models import Artist, ArtistList
from .util import ERRORS

aura = Flask(__name__)
api = Api(aura, prefix="/aura/v0.1", errors=ERRORS)
api.decorators = [cors.crossdomain(origin="*", methods=['GET','OPTIONS'])]

api.add_resource(Aura, '/', '/server', '/aura')
api.add_resource(Artist, '/artists/<int:artist_id>')
api.add_resource(ArtistList, '/artists')
api.add_resource(Track, '/tracks/<int:track_id>')
api.add_resource(TrackList, '/tracks')
api.add_resource(TrackAudio, '/tracks/<int:track_id>/audio')
api.add_resource(Album, '/albums/<int:album_id>')
api.add_resource(AlbumList, '/albums')
api.add_resource(Stats, '/stats')

@aura.before_request
def before_request():
    g.lib = Library(aura.config['LIBRARY_DB_PATH'],aura.config['MUSIC_DIR'])


if __name__ == '__main__':
    aura.run(debug=True)


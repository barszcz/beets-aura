#!/usr/bin/env python

from flask import Flask, g
from flask_restful import Api

from beets.library import Library
from .models import Aura, Stats
from .models import Track, TrackList
from .models import Album, AlbumList
from .models import Artist, ArtistList

aura = Flask(__name__)
api = Api(aura, prefix="/aura/v0.1")

api.add_resource(Aura, '/')
api.add_resource(Artist, '/artists/<int:artist_id>')
api.add_resource(ArtistList, '/artists')
api.add_resource(Track, '/tracks/<int:track_id>')
api.add_resource(TrackList, '/tracks')
api.add_resource(Album, '/albums/<int:album_id>')
api.add_resource(AlbumList, '/albums')
api.add_resource(Stats, '/stats')

@aura.before_request
def before_request():
    g.lib = Library('/home/gabeos/.config/beets/library.db','/home/gabeos/music_library')


if __name__ == '__main__':
    aura.run(debug=True)



from flask import g
from flask_restful import Resource, marshal_with
import flask_restful.fields as rf

class Album(Resource):
    '''Endpoint for a single album'''

    fields = {
		#'albumartist_credit': rf.String,
		#'albumartist_sort': rf.String,
		#'albumdisambig': rf.String,
		#'albumstatus': rf.String,
		#'original_day': rf.String,
		#'original_month': rf.String,
		#'original_year': rf.String,
		#'script': rf.String,
        'added': rf.Float,
        'albumtype': rf.String,
		'artist': rf.String(attribute='albumartist'),
		'artpath': rf.String,
		'asin': rf.String,
		'catalognum': rf.String,
		'comp': rf.Boolean,
		'country': rf.String,
		'day': rf.Integer,
        'disctotal': rf.Integer,
        'genre': rf.List(rf.String, attribute=lambda x: [x['genre']]),
		'id': rf.String,
		'label': rf.String,
		'language': rf.String,
        'links': {'tracks': rf.List(rf.String, attribute='track_ids')},
		'mb_albumartistid': rf.String,
		'month': rf.Integer,
		'release_group_mbid': rf.String(attribute='mb_releasegroupid'),
		'release_mbid': rf.String(attribute='mb_albumid'),
		'rg_album_gain': rf.String,
		'rg_album_peak': rf.String,
		'title': rf.String(attribute='album'),
		'year': rf.Integer
    }

    @classmethod
    def _conv_album(cls,album):
        album_info = dict(album)
        track_ids = [i['id'] for i in album.items()]
        album_info['track_ids'] = track_ids
        return album_info


    @marshal_with(fields, envelope='albums')
    def get(self, album_id):
        album = g.lib.get_album(album_id)
        return Album._conv_album(album)

class AlbumList(Resource):
    '''Endpoint for the full list of Albums'''

    fields = {
        'albums': rf.List(rf.Nested(Album.fields))
    }

    @marshal_with(fields)
    def get(self):
        return {'albums': map(Album._conv_album, g.lib.albums())}


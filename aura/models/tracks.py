
import os.path as path
from flask import g
from flask_restful import Resource, marshal_with
import flask_restful.fields as rf

class Track(Resource):
    '''Endpoint for a single track'''
    def get_file_size(track_info):
        if path.isfile(track_info['path']):
            return path.getsize(track_info['path'])
        else:
            return 0

    fields = {
        #'albumartist_credit': rf.String,
        #'albumartist_sort': rf.String,
        #'albumdisambig': rf.String,
        #'albumstatus': rf.String,
        #'artist_credit': rf.String,
        #'artist_sort': rf.String,
        #'encoder': rf.String,
        #'grouping': rf.String,
        #'initial_key': rf.String,
        #'mb_albumartistid': rf.String,
        #'mb_albumid': rf.String,
        #'mb_artistid': rf.String,
        #'mb_releasegroupid': rf.String,
        #'mtime': rf.Float,
        #'original_day': rf.Integer,
        #'original_month': rf.Integer,
        #'original_year': rf.Integer,
        #'path': rf.String,
        #'script': rf.String,
        'acoustid_fingerprint': rf.String,
        'acoustid_id': rf.String,
        'added': rf.Float,
        'album': rf.String,
        'album_id': rf.Integer,
        'albumartist': rf.String,
        'albumtype': rf.String,
        'artist': rf.List(rf.String, attribute=lambda a: [a['artist']]),
        'asin': rf.String,
        'bitdepth': rf.Integer,
        'bitrate': rf.String,
        'bpm': rf.Integer,
        'catalognum': rf.String,
        'channels': rf.Integer,
        'comments': rf.String,
        'comp': rf.Integer,
        'composer': rf.List(rf.String, attribute=lambda t: [t['composer']]),
        'country': rf.String,
        'day': rf.Integer,
        'disc': rf.Integer,
        'disctitle': rf.String,
        'disctotal': rf.Integer,
        'duration': rf.Float(attribute='length'),
        'genre': rf.List(rf.String, attribute=lambda t: [t['genre']]),
        'id': rf.String,
        'label': rf.String,
        'language': rf.String,
        'lyrics': rf.String,
        'media': rf.String,
        'month': rf.Integer,
        'rg_album_gain': rf.Float,
        'rg_album_peak': rf.Float,
        'rg_track_gain': rf.Float,
        'rg_track_peak': rf.Float,
        'samplerate': rf.Integer,
        'size': rf.Integer(attribute=get_file_size),
        'title': rf.String,
        'track': rf.Integer,
        'track_mbid': rf.String(attribute='mb_trackid'),
        'tracktotal': rf.Integer,
        'type': rf.String(attribute='format'), # TODO Convert to actual MIME type
        'year': rf.Integer,
        'links': {
            # TODO implement artist links
            'albums': rf.List(rf.String, attribute=lambda t: [t['album_id']])
        }
    }

    @marshal_with(fields)
    def get(self, track_id):
        return dict(g.lib.get_item(track_id))

class TrackList(Resource):
    '''Endpoint for full list of tracks'''
    fields = {
        'tracks': rf.List(rf.Nested(Track.fields))
    }

    @marshal_with(fields)
    def get(self):
        return { 'tracks': g.lib.items() }



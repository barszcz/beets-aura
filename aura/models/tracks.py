
import os.path as path
import mimetypes
from flask import g, Response
from flask_restful import Resource, marshal_with, reqparse
import flask_restful.fields as rf
from ..util import sort_accept_headers, AcceptHeader
from ..util import conversion_stream, file_stream, conversion_formats
import logging

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

    @marshal_with(fields, envelope="tracks")
    def get(self, track_id):
        return {k: v for (k, v) in dict(g.lib.get_item(track_id)).iteritems() if v is not None and v is not "" }

class TrackList(Resource):
    '''Endpoint for full list of tracks'''
    fields = {
        'tracks': rf.List(rf.Nested(Track.fields))
    }

    @marshal_with(fields)
    def get(self):
        return { 'tracks': g.lib.items() }


class TrackAudio(Resource):
    logger = logging.getLogger(__name__)

    def get(self, track_id):

        # TODO: Convert depending content-type
        # TODO: Set response headers -- content-type, x-sendfile,
        #       content-disposition
        # TODO: send_file or error

        parser = reqparse.RequestParser(trim=True)
        parser.add_argument('Accept', location='headers', default='audio/*')
        parser.add_argument('Negotiate', location='headers')
        parser.add_argument('Range', location='headers')
        args = parser.parse_args()

        accepts = sort_accept_headers(args['Accept'], 'audio/*')
        self.logger.debug('sorted accept headers: {}'.format(accepts))

        best_fmt = \
            next((p for p in accepts \
                  if not conversion_formats.isdisjoint(p.extensions)),
                 AcceptHeader('audio/*')) \
            if accepts else AcceptHeader('audio/*')
        self.logger.debug('Best Accepted format: {}'.format(best_fmt))
        print 'Best Accepted format: {}'.format(best_fmt)

        track_info = g.lib.get_item(track_id)
        audio_fn = track_info['path']
        fmt_ext = path.split(audio_fn)[1]
        audio_mime = AcceptHeader(mimetypes.guess_type(audio_fn)[0])
        print 'Audio Mime: {}'.format(audio_mime)
        if audio_mime.matches(best_fmt):
            fsize = path.getsize(audio_fn)
            print 'FileSize: {}'.format(fsize)
            resp = Response(file_stream(audio_fn),
                            track_info['bitrate'],
                            mimetype=audio_mime.mimetype,
                            direct_passthrough=True)
            resp.headers['Content-Length'] = fsize
        else:
            fmt_ext = mimetypes.guess_extension(best_fmt.mimetype)
            resp = Response(
                conversion_stream(
                    audio_fn,fmt_ext,
                    best_fmt.parameters.get('bitrate'))[0],
                mimetype=best_fmt.mimetype,
                direct_passthrough=True)

        resp.headers['Content-Disposition'] = "{} - {} {}.{}".format(
            track_info['artist'], track_info['track'],
            track_info['title'], fmt_ext )
        resp.status_code=200

        return resp



from flask import g
from flask_restful import Resource



class Artist(Resource):
    '''Endpoint for specific artists'''

    def get(self, artist_id):
        raise NotImplementedError()

class ArtistList(Resource):
    '''Endpoint for all artists'''
    def get(self):
        with g.lib.transaction() as tx:
            rows = tx.query("SELECT DISTINCT albumartist FROM albums")
        all_artists = [row[0] for row in rows]
        return {'artist_names': all_artists }



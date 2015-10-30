
from flask_restful import Resource
from flask import g

class Stats(Resource):
    '''Endpoint for statistics about the music library

    Although out of spec for AURA, it seems useful for most frontend apps
    '''

    def get(self):
        with g.lib.transaction() as tx:
            item_rows = tx.query("SELECT COUNT(*) FROM items")
            album_rows = tx.query("SELECT COUNT(*) FROM albums")
        return {
                'items': item_rows[0][0],
                'albums': album_rows[0][0],
            }


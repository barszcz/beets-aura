
from flask_restful import Resource

class Aura(Resource):
    '''Endpoint for server API info
    '''

    def get(self):
        return {
            'server': {
                'aura-version': '0.1.0',
                'host': 'beets-aura',
                'host-version': '0.1.0',
                'auth-required': False,
                'features': ['albums', 'artists']
            }
        }, 200

#@aura.route('/item/query/')
#def all_items():
#    return g.lib.items()
#
#
#@aura.route('/item/<int:item_id>/stream')
#def item_file(item_id):
#    item = g.lib.get_item(item_id)
#    response = send_file(item.path, as_attachment=True,
#                                   attachment_filename=os.path.basename(item.path))
#    response.headers['Content-Length'] = os.path.getsize(item.path)
#    return response
#
#
#@aura.route('/item/query/<string:query>')
#def item_query(queries):
#    return g.lib.items(queries)
#
#
## Albums.
#
#@aura.route('/album/')
#@aura.route('/album/query/')
#def all_albums():
#    return g.lib.albums()
#
#
#@aura.route('/album/query/<query:queries>')
#def album_query(queries):
#    return g.lib.albums(queries)
#
#@aura.route('/album/<int:album_id>/art')
#def album_art(album_id):
#    album = g.lib.get_album(album_id)
#    return send_file(album.artpath)



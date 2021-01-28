import falcon

from .images import Resource


api = application = falcon.API()

images = Resource()
api.add_route('/images', images)
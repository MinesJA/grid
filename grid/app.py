import falcon
from .images import Resource




def main():
    api = application = falcon.API()

    images = Resource()
    api.add_route('/images', images)
    




if __name__ '__main__':
    main()
import falcon
from .images import Resource

def main():
    # Setup controllers/Routes with Falcon
    api = application = falcon.API()
    images = Resource()
    api.add_route('/images', images)

    # Load/Build Grid from yaml file
    Grid.build()
    
    # Start timer
    TimeService().start

    # Check Grid for total in, total out





if __name__ == '__main__':
    main()
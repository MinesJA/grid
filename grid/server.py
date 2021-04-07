from falcon import asgi
import argparse
from grid.resources.messages import Messages
from grid.models.node import NodeBuilder


def create_app(args):
    app = asgi.App()
    builder = NodeBuilder(id=args.id, address=args.address,
                          port=args.port, pro=10, con=5)
    messages = Messages(builder)
    app.add_route('/ask/{type}', messages, suffix='ask')
    app.add_route('/tell/{type}', messages, suffix='tell')

    app.add_route('/nodes/siblings', messages, suffix='siblings')
    app.add_route('/nodes/energy', messages, suffix='energy')
    return app


def parse_args(args):
    return create_parser().parse_args(args)


def create_parser():
    parser = argparse.ArgumentParser(description='Start a node')
    parser.add_argument('--id', '-i')
    parser.add_argument('--address', '-a')
    parser.add_argument('--port', '-p', type=int)
    return parser

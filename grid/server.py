from falcon import asgi
import argparse
from grid.resources.messages import Messages
from grid.resources.nodes import Nodes


def create_app(node_builder):
    app = asgi.App()

    messages = Messages(node_builder)
    nodes = Nodes(node_builder)

    app.add_route('/ask/{type}', messages, suffix='ask')
    app.add_route('/tell/{type}', messages, suffix='tell')

    app.add_route('/nodes/siblings', nodes, suffix='siblings')
    app.add_route('/nodes/energy', nodes, suffix='energy')
    return app


def parse_args(args):
    return create_parser().parse_args(args)


def create_parser():
    parser = argparse.ArgumentParser(description='Start a node')
    parser.add_argument('--id', '-i')
    parser.add_argument('--address', '-a')
    parser.add_argument('--port', '-p', type=int)
    return parser

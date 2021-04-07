from falcon import asgi
import argparse
import sys


from grid.resources.messages import Messages
from grid.models.node import NodeBuilder

def create_app():
    args = parse_args()
    app = asgi.App()
    builder = NodeBuilder(id=args.id, address=args.address, port=args.port, pro=10, con=5)
    messages = Messages(builder)
    app.add_route('/messages', messages)
    return app

def parse_args():
    parser = argparse.ArgumentParser(description='Start a node')
    parser.add_argument('--id', '-i')
    parser.add_argument('--address', '-a')
    parser.add_argument('--port', '-p', type=int)
    return parser.parse_args(sys.argv[1:])
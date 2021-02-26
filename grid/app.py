import falcon
import uuid
from gunicorn.app.base import BaseApplication
from grid.resources.powerResource import PowerResource
from grid.resources.nodeResource import NodeResource
from grid.services.task_service import TaskService
from grid.models.node import Node
import multiprocessing
import argparse
import sys


# Todo: Build node with address and port, start server with same address and port

def create_app(task_service, node):
    api = application = falcon.API()
    power_resource = PowerResource(task_service, node)
    node_resource = NodeResource(task_service, node)
    api.add_route('/power', power_resource)
    api.add_route('/nodes', node_resource)
    return api


def get_app():
    task_service = TaskService()
    args = parse_args()
    id = uuid.uuid1()
    print(str(id))
    node = Node(id=id, address=args.address, port=args.port)
    return create_app(task_service, node)


def parse_args():
    parser = argparse.ArgumentParser(description='Start a node')
    parser.add_argument('--address', '-a')
    parser.add_argument('--port', '-p')
    return parser.parse_args(sys.argv[1:])


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


def get_options():
    args = parse_args()
    return {
        'bind': '%s:%s' % (args.address, args.port),
        'workers': number_of_workers(),
        'reload': True,
        'debug': True,
        'loglevel': 'debug'
    }


class StandaloneApplication(BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    StandaloneApplication(get_app(), get_options()).run()

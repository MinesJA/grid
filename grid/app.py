import falcon
import uuid
from gunicorn.app.base import BaseApplication
from grid.resources.powerResource import PowerResource
from grid.resources.nodeResource import NodeResource
from grid.services.task_service import TaskService
from grid.models.node import Node
import multiprocessing
import gunicorn.app.base
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
    parser = argparse.ArgumentParser(description='Start a node')
    parser.add_argument('--address', '-a')
    parser.add_argument('--port', '-p')
    args = parser.parse_args(sys.argv[1:])

    task_service = TaskService()
    node = Node(address=args.address, port=args.port)
    return create_app(task_service, node)


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


def get_options():
    return {
        'bind': '%s:%s' % ('127.0.0.1', '8080'),
        'workers': number_of_workers(),
    }


class StandaloneApplication(gunicorn.app.base.BaseApplication):

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

    StandaloneApplication(get_app(), options).run()

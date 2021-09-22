from grid.serializer import deserialize, serialize
import falcon
import falcon.asgi
from falcon import media
from grid.resources.messaging import Messaging
import uvicorn


class Server(uvicorn.Server):
    def __init__(self, inbox, loop, host, port):
        # self.inbox = inbox
        # self.loop = loop
        # self.host = host
        # self.port = port

        app = self.__create_app(inbox)
        config = uvicorn.Config(app=app, host=host,
                                port=port, loop=loop)
        super(config)

    def install_signal_handlers(self):
        pass

    def __call__(self):
        self.serve()

    def __create_app(self, inbox):
        app = falcon.asgi.App()
        json_handler = media.JSONHandler(
            loads=deserialize,
        )
        extra_handlers = {
            'application/json': json_handler,
        }

        app.req_options.media_handlers.update(extra_handlers)
        app.resp_options.media_handlers.update(extra_handlers)

        messaging = Messaging(inbox=inbox)
        app.add_route('/messaging', messaging)
        return app

    def exit(self):
        self.should_exit = True

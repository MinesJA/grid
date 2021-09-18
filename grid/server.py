import contextlib
import time
import threading
import uvicorn

# TODO: Do I need these imports?


class Server(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    def exit(self):
        self.should_exit = True

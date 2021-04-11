import contextlib
import time
import threading
import uvicorn


class Server(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    def exit(self):
        self.should_exit = True

from grid.services import Service
import time
import threading
import schedule


class Scheduler(Service):

    def __init__(self, callable, interval):
        self.callable = callable
        self.interval = interval
        self.stop = None

    async def __call__(self):
        """Continuously run, while executing pending jobs at each
        elapsed time interval.
        @return cease_continuous_run: threading. Event which can
        be set to cease continuous run. Please note that it is
        *intended behavior that run_continuously() does not run
        missed jobs*. For example, if you've registered a job that
        should run every minute and you set a continuous run
        interval of one hour then your job won't be run 60 times
        at each interval but only once.
        """
        times = [f":{x:02}" for x in range(60) if x % self.interval == 0]

        for time in times:
            schedule.every().minute.at(time).do(self.callable)

        self.should_stop = threading.Event()

        class ScheduleThread(threading.Thread):
            @ classmethod
            def run(cls):
                while not self.cease_run.is_set():
                    schedule.run_pending()
                    time.sleep(self.interval)

        print("RUNNING clockcycle")

        continuous_thread = ScheduleThread()
        continuous_thread.start()

    def exit(self):
        self.should_stop.set()

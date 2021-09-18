import time
import datetime
import threading
import schedule


class JobWrapper:

    def __init__(self, interval, job):
        self.interval = interval
        self.job = job

    def start(self):
        self.interval.do(self.job)


class Scheduler:

    def __init__(self, jobs):
        self.jobs = jobs
        self.cease_run = None

    @classmethod
    def every(clss, interval, job):
        times = [f":{x:02}" for x in range(60) if x % interval == 0]
        jobs = [JobWrapper(schedule.every().minute.at(x), job)
                for x in times]

        return clss(jobs)

    def background_job():
        print(datetime.datetime.utcnow())

    def schedule_jobs(self):
        for job in self.jobs:
            job.start()

    def stop(self):
        self.cease_run.set()

    def start(self, interval=1):
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
        self.schedule_jobs()

        self.cease_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @ classmethod
            def run(cls):
                while not self.cease_run.is_set():
                    schedule.run_pending()
                    time.sleep(interval)

        print("RUNNING clockcycle")

        continuous_thread = ScheduleThread()
        continuous_thread.start()

import queue


class TaskService(object):

    def __init__(self):
        self.queue = queue.Queue()

    def add_task(self, task):
        self.queue.put(task)
    
    def start_processing(self):
        while not self.queue.empty():
            task = self.queue.get()
            print(task)
            task.execute()
        



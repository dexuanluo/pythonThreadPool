# _*_ encoding=utf-8 _*_
import threading
import psutil
from threadpool.task import Task, AsyncTask
from threadpool.queue import ThreadingSafeQueue, ThreadingSafeQueueException
class ProcessThread(threading.Thread):
    def __init__(self, task_queue, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.dismiss_flag = threading.Event()
        self.task_queue = task_queue
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
        while True:
            if self.dismiss_flag.is_set():
                break
            item = self.task_queue.pop()
            if not isinstance(item, Task):
                continue
            result = item.callable(*item.args, **item.kwargs)
            if isinstance(item, AsyncTask):
                item.set_result(result)
    def stop(self):
        self.dismiss_flag.set()

class ThreadPool:
    def __init__(self, size = 0):
        if not size:
            """
            by default 2 times of the # of cpu
            """
            size = psutil.cpu_count() * 2

        self.pool = ThreadingSafeQueue(size)
        self.task_queue = ThreadingSafeQueue()
        for _ in range(size):
            self.pool.put(ProcessThread(self.task_queue))
    def start(self):
        for i in range(self.pool.size()):
            thread = self.pool.get(i)
            thread.start()
    def join(self):
        for i in range(self.pool.size()):
            thread = self.pool.get(i)
            thread.stop()
        while self.pool.size():
            thread = self.pool.pop()
            thread.join()
            
    def put(self, item):
        if not isinstance(item, Task):
            raise TaskTypeErrorException()
        self.task_queue.put(item)
    
    def batch_put(self, item_list):
        if not isinstance(item_list, list):
            item_list = list(item_list)
        for item in item_list:
            self.put(item)
    def size(self):
        return self.pool.size()



class TaskTypeErrorException(Exception):
    pass
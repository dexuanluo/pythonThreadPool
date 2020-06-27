import uuid
import threading
class Task:
    def __init__(self, func, *args, **kwargs):
        self.callable = func
        self.id = uuid.uuid4()
        self.args = args
        self.kwargs = kwargs
    def __str__(self):
        return "Create Task: " + str(self.id)

class AsyncTask(Task):
    def __init__(self, func, *args, **kwargs):
        self.res = None
        self.condition = threading.Condition()
        super().__init__(func, *args, **kwargs)


    def set_result(self, result):
        self.condition.acquire()
        self.res = result
        self.condition.notify()
        self.condition.release()
        
    def get_result(self):
        self.condition.acquire()
        if not self.res:
            self.condition.wait()
        result = self.res
        self.condition.release()
        return result
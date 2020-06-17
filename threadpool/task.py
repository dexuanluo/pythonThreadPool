import uuid

class Task:
    def __init__(self, func, *args, **kwargs):
        self.callable = func
        self.id = uuid.uuid4()
        self.args = args
        self.kwargs = kwargs
    def __str__(self):
        return "Create Task: " + str(self.id)
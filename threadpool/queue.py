import threading
import time
class ThreadingSafeQueueException(Exception):
    pass
class ThreadingSafeQueue(object):
    def __init__(self, max_size = 0):
        self.queue = []
        self.max_size = max_size
        self.lock = threading.Lock()
        self.condition = threading.Condition()
    
    def size(self):
        self.lock.acquire()
        size = len(self.queue)
        self.lock.release()
        return size
    
    def put(self, item):
        if self.max_size != 0 and self.size() > self.max_size:
            return ThreadingSafeQueueException()
        self.lock.acquire()
        self.queue.append(item)
        self.lock.release()
        
    
    def batch_put(self, item_list):
        if not isinstance(item_list, list):
            item_list = list(item_list)
        for item in item_list:
            self.put(item)
    
    def pop(self, block = False, timeout = None):
        if self.size() == 0:
            if block:
                self.condition.acquire()
                self.condition.wait(timeout = timeout)
                self.condition.release()
            else:
                return
        
        self.lock.acquire()
        if len(self.queue) > 0:
            item = self.queue.pop()
            self.lock.release()
            return item
        else:
            return None
    
    def get(self, index):
        self.lock.acquire()
        item = self.queue[index]
        self.lock.release()
        return item
    
if __name__ == "__main__":
    q = ThreadingSafeQueue(max_size = 100)
    def producer():
        while True:
            q.put(1)
            time.sleep(1)
            print(q.queue)
    def consumer():
        while True:
            item = q.pop(block = True, timeout = 2)
            print(f"get item from queue: {item}")
            time.sleep(1)
        
    t1 = threading.Thread(target = producer)
    t2 = threading.Thread(target = consumer)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

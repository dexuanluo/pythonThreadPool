from threadpool import task, pool
import time
import threading

def test_async_task():

    def async_process():
        num = 0
        for i in range(100):
            num += i
        time.sleep(5)
        return num


    test_pool = pool.ThreadPool()
    test_pool.start()
    for i in range(10):
        async_task = task.AsyncTask(func = async_process)
        test_pool.put(async_task)
        print("get result at ",time.time())
        result = async_task.get_result()
        print("result: ", result)

test_async_task()


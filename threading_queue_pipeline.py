# Author: gabri
# File: threading_queue_pipeline
# Date: 11/07/2019
# Made with PyCharm

# Standard Library
from threading import Thread, Lock
from time import sleep, time
from queue import Queue

# Third party modules

# Local application imports

lock = Lock()


def download(arg):
    with lock:
        print('download')
    sleep(0.01)
    return 1


def resize(arg):
    with lock:
        print('resize')
    sleep(0.005)
    return 2


def upload(arg):
    with lock:
        print('upload')
    sleep(0.05)
    return 3


class ClosableQueue(Queue):
    sentinel = object()

    def close(self):
        self.put(self.sentinel)

    def __iter__(self):
        # If there is an item to get, continue. If there isn't, wait.
        while True:
            # Uses try just to use finally. Even if the return statement is
            # reached, the finally statement will be called. Every time you
            # put an ellement on the queue, you need to call task_done().
            # Every time you enqueue an item, it will automatically increase an
            # internal counter, using task_done() decrement it. When you call
            # join(), it will run the thread until the internal counter is zero.
            # If you called task_done() poorly, the thread will never end when
            # you join() it.
            try:
                item = self.get()
                if item is self.sentinel:
                    return
                yield item
            finally:
                self.task_done()


class Worker(Thread):
    def __init__(self, function, in_queue, done_queue):
        super().__init__()
        self.function = function
        self.in_queue = in_queue
        self.done_queue = done_queue

    def run(self):
        for item in self.in_queue:
            result = self.function(item)
            self.done_queue.put(result)


def main():
    # Arguments on the queue are the buffer size. Interesting when you know
    # some final task is the funnel of the some process.
    download_queue = ClosableQueue(1000)
    resize_queue = ClosableQueue(100)
    upload_queue = ClosableQueue(5)
    done_queue = Queue()
    threads = [Worker(download, download_queue, resize_queue),
               Worker(resize, resize_queue, upload_queue),
               Worker(upload, upload_queue, done_queue)]

    # Start the threads, even if there are not items to process yet
    start_time = time()
    for thread in threads:
        thread.start()

    for _ in range(200):
        download_queue.put(object())
    download_queue.close()
    download_queue.join()
    resize_queue.close()
    resize_queue.join()
    upload_queue.close()
    upload_queue.join()
    print(done_queue.qsize(), 'items finished')
    print('Took {:.3f} seconds'.format(time() - start_time))


if __name__ == "__main__":
    main()

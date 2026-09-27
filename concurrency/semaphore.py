# Implement your own semaphore class that can be used as a context manager, 
# then write a short program demonstrating that it limits how many threads can access a shared resource at the same time.

import threading
import time
import random

class Semaphore:
    def __init__(self, capacity=1):
        self.capacity = capacity
        self.used = 0
        self.cond = threading.Condition()

    def __enter__(self):
        with self.cond:
            while self.used == self.capacity:
                print(f"waiting to acquire semaphore")
                self.cond.wait()
            self.used += 1
            self.cond.notify_all()
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with self.cond:
            self.used -= 1
            self.cond.notify_all()
        return 

def run(id, sem):
    with sem:
        print(f"Thread {id} running")
        time.sleep(random.random())
        print(f"Thread {id} completed")


def main():

    sem = Semaphore(2)
    tasks = []

    for i in range(10):
        tasks.append(threading.Thread(target=run, args=(i, sem) ))

    for task in tasks:
        task.start()
    for task in tasks:
        task.join()


if __name__ == "__main__":
    main()
# Task 7: Worker Pool with Shutdown Event
# Build a small worker system using threading.Event.
# Create
# class Worker
# State:
# a worker ID
# a threading.Event used as a shutdown signal
# some shared collection of jobs
# Implement:
# run()
# stop()
# Behavior
# Create 3 worker threads.
# Each worker should:
# Repeatedly check whether there is work to process.
# Process available jobs.
# Continue working until the shutdown event is set.
# Once shutdown is signaled, finish its current job if it is already processing one, then exit.
# The main thread should:
# Create a batch of jobs.
# Start the 3 workers.
# Allow them to process jobs for a while.
# Signal shutdown using the Event.
# Wait for all workers to terminate.

import threading
from collections import deque
import time 
import random

class Worker:
    def __init__(self, id, jobs):
        self.id = id 
        self.jobs = jobs
        self.done = threading.Event()
        self.lock = threading.Lock()
    
    def run(self):
        with self.lock:
            while self.jobs and not self.done:
                print(f"Running job {self.jobs.popleft()}")
                time.sleep(random.random())

    def stop(self):
        with self.lock:
            self.done.set()

            

def main():


    # Create shared jobs
    jobs = deque()
    for i in range(50):
        jobs.append(i)

    # Create workers
    num_workers = 3
    workers = []

    for i in range(num_workers):
        workers.append(Worker(i, jobs))

    for worker in workers:
        worker.run()

    for worker in workers:
        worker.stop()


if __name__ == "__main__":
    main()
  

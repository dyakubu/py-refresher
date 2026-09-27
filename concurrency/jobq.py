# Task 4: Producer/Consumer with threading.Condition
# Now practice a different synchronization problem: threads waiting for a state to change.
# Build a JobQueue class.
# State
# The class should maintain:
# A list of pending jobs
# A maximum capacity of 5
# A threading.Condition
# A way to indicate that producers are finished
# Methods
# Implement:
# put(job)
# If the queue is full, wait
# Otherwise add the job
# Wake up a waiting consumer
# get()
# If the queue is empty but producers may still produce, wait
# Otherwise remove and return a job
# Wake up a waiting producer
# close()
# Indicate that no more jobs will be added
# Wake up any consumers currently waiting
# Concurrency setup
# Create:
# 2 producer threads
# 2 consumer threads
# Each producer should generate 50 jobs.
# Each consumer should repeatedly retrieve and process jobs until there are:
# No jobs remaining, and
# No producers left that could generate more jobs.
# Have consumers sleep briefly when processing a job so you can actually observe the producer/consumer interaction.


import threading
from collections import deque
import time

class JobQueue:
    def __init__(self, maxSize):

        self.maxSize = maxSize
        self.jobs = deque()
        self.cond = threading.Condition()
        self.closed = False
 
    def put(self, job):
        with self.cond:
            # The while, not if here here is important. While cond is waiting, it frees the lock
            # So another thread could have filled up the quque again in the intervening period
            while len(self.jobs) >= self.maxSize:
                self.cond.wait() 
            self.jobs.append(job)
            self.cond.notify_all()

    def get(self):
        with self.cond:
            while len(self.jobs) == 0 and not self.closed:
                self.cond.wait()
            if len(self.jobs) == 0 and self.closed:
                return None
            job =  self.jobs.popleft() 
            self.cond.notify_all()
            return job
    
    def close(self):
        with self.cond:
            self.closed = True
            self.cond.notify_all()
      
def produce(jobq, num_jobs):
    for i in range(num_jobs):
        print(f"producing job id {i}")
        jobq.put(i)
        print(f"Produced id {i} successfully")

def consume(jobq):
    while True:
        job = jobq.get()
        if job is None:
            break
        print(f"consuming job id {job}")
        time.sleep(1)    
        print(f"Job id {job} consumed successfully")

def main():
    
    q = JobQueue(maxSize=5)
    # Producers
    producers = []
    # Consumers
    consumers = []

    for i in range(2):
        producers.append(threading.Thread(target=produce, args=(q, 50)))
    
    # Consumers
    for i in range(2):
        consumers.append(threading.Thread(target=consume, args=(q,)))

    for c in consumers:
        c.start()
    for p in producers:
        p.start()

    for p in producers:
        p.join()
    q.close()

    for c in consumers:
        c.join()

if __name__ == "__main__":
    main()
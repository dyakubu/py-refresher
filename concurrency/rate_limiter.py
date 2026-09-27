# Task 6: Thread-Safe Rate Limiter
# Build a thread-safe rate limiter using threading.Lock.
# Requirements
# Create:
# class RateLimiter:
# State:
# limit: maximum number of requests allowed
# window: time window in seconds
# internal state to track recent requests
# a threading.Lock
# Implement:
# allow()
# Behavior:
# Return True if the request is allowed.
# Return False if the caller has exceeded the limit within the current time window.
# The implementation must be thread-safe.
# Multiple threads may call allow() concurrently.

import threading 
import time
import random

class RateLimiter:
    def __init__(self, limit, window):
        self.window = window 
        self.limit = limit 
        self.start = time.time()
        self.end = self.start + window
        self.requests = 0
        self.lock = threading.Lock()

    def allow(self):
        with self.lock:
            request_time = time.time()
            if request_time < self.end and self.requests < self.limit:
                self.requests += 1
                return True 
            elif request_time > self.end:
                self.start = time.time()
                self.end = self.start + self.window
                self.requests += 1
                return True 
            else:
                return False


    

def make_request(rl, id):
    if rl.allow():
        print(f"Request {id} allowed")
        time.sleep(random.random())
        return 
    print(f"Request {id} denied")
    

def main():

    rl = RateLimiter(2, 1)
    tasks = []

    for i in range(10):
        tasks.append(threading.Thread(target=make_request, args=(rl, i)))

    for task in tasks:
        task.start()

    for task in tasks:
        task.join()
    

if __name__ == "__main__":
    main()
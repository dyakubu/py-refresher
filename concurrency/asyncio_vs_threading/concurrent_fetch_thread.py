# # Task 1 — Concurrent API Fetcher
# # Build a program that fetches data from multiple URLs concurrently.
# Fetch every URL.
# Return the response status code for each URL.
# Run the requests concurrently.
# Record how long each request took.
# If a request fails, record the failure rather than terminating the entire program.
# Limit concurrency to 5 simultaneous requests.
# The caller should receive the results in the same order as the input URLs.

import threading 
import requests 
import time
from dataclasses import dataclass

@dataclass(frozen=True)
class FetchResponse:
    request_url: str 
    response_status_code: int | None
    elapsed_time: float 
    exc: Exception | None


class ConcurrentURLFetcher:

    def __init__(self, max_concurrent=2, timeout=5.0):
        self.max_concurrent = max_concurrent
        self.sem = threading.Semaphore(max_concurrent)
        self.timeout = timeout

    # Semaphore protected. At most max_concurrent requests running concurrently
    def fetch_url(self, url, i, results):

        with self.sem:
            start = time.perf_counter()
            try:
                res = requests.get(url, timeout=self.timeout)
                results[i] = FetchResponse(url, res.status_code, elapsed_time= time.perf_counter() - start, exc=None)
            except requests.RequestException as E:
                results[i] = FetchResponse(url, response_status_code=None, elapsed_time=time.perf_counter() - start, exc=E)
    
    def fetch_urls(self, urls):

        tasks = []
        results = [None] * len(urls)

        for i in range(len(urls)):
            tasks.append(threading.Thread(target=self.fetch_url, args=(urls[i], i, results)))
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()
        return results





def main():

    URLS = ["https://google.com", "https://linkedin.com", "https://jargonblahnonexistent.com", "https://youtube.com"]

    f = ConcurrentURLFetcher(2)
    
    q = f.fetch_urls(URLS)
    [print(res, url) for res, url in zip(q, URLS)]


    
if __name__ == "__main__":
    main()
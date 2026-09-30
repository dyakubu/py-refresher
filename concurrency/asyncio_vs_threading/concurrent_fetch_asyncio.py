# # Task 1 — Concurrent API Fetcher
# # Build a program that fetches data from multiple URLs concurrently.
# Fetch every URL.
# Return the response status code for each URL.
# Run the requests concurrently.
# Record how long each request took.
# If a request fails, record the failure rather than terminating the entire program.
# Limit concurrency to 5 simultaneous requests.
# The caller should receive the results in the same order as the input URLs.

from dataclasses import dataclass 
import asyncio 
import httpx 

@dataclass(frozen=True)
class FetchResponse:
    status_code: int | None 
    exc: Exception | None 
    elapsed_time: float | None 

class ConcurrentAPIFetcher:

    def __init__(self, max_concurrent, timeout):
        self.max_concurrent = max_concurrent 
        self.timeout = timeout 

    async def fetch_urls(self, URLs):

        coros = []

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            async with asyncio.Semaphore(self.max_concurrent):
                for url in URLs:
                    coros.append(client.get(url))

            return await asyncio.gather(*coros)
    


async def main():

    URLS = ["https://linkedin.com", "https://google.com", "https://htsrtaygarbageurl", "https://github.com"]

    f = ConcurrentAPIFetcher(5, 10)
    r = await f.fetch_urls(URLS)
    print(r)


    

if __name__=="__main__":
    asyncio.run(main())
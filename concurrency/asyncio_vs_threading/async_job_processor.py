# Build an asynchronous job-processing system.
# Requirements
# You have an arbitrary number of jobs:
# job 1
# job 2
# job 3
# ...
# job 20
# Each job is represented by an integer ID.
# You have this async API:
# process_job(job_id) -> result
# # Your system should:
# # Have 2 producers.
# # Have 3 consumers.
# # Use an asyncio.Queue with a maximum capacity of 5.
# # Each producer should generate 10 jobs.
# # Consumers should continuously take jobs from the queue and process them.
# # A consumer should not start another job until its current job finishes.
# # Wait until all jobs have been processed before shutting down.
# # Shut down the consumers cleanly.
# # If process_job() raises an exception, don't crash the entire system. Record/report the failed job and continue processing other jobs.
# # Use only asyncio. No threads, no queue.Queue, no Semaphore.
# # Important constraint
# # Don't use asyncio.gather() to simply launch 20 process_job() calls.
# # The point is to actually build: 

import asyncio 
import random 
import time

async def process_job(id):
    await asyncio.sleep(3)
    if random.randint(1,10) < 7:
        print(f"Job {id} processed successfully!")
        return 
    raise RuntimeError(f"Job {id} FAILED!")

async def produce(q, num_jobs):
    for _ in range(num_jobs):
        await q.put(time.monotonic())

async def consume(q):
    while True:
        job = await q.get()
        if job == "sentinel":
            q.task_done()
            break
        try:
            await process_job(job)
        except RuntimeError as e:
            print(f"Runtime error, {e}")
        finally:
            q.task_done()
        
    return 
    
async def main():
    q = asyncio.Queue(maxsize=5)
    num_jobs = 10
    producers = []
    consumers = []

    for _ in range(2):
        producers.append(asyncio.create_task(produce(q, num_jobs)))
    for _ in range(3):
        consumers.append(asyncio.create_task(consume(q)))

    await asyncio.gather(*producers)
    await q.join()
    for i in range(len(consumers)):
        await q.put("sentinel")
    await asyncio.gather(*consumers)


    

if __name__ == "__main__":
    asyncio.run(main())


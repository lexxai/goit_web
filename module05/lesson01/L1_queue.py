import asyncio
import random
import time


async def io_bound(info: str, queue: asyncio.Queue):
    value = await queue.get()
    print("io_bound start", info, value)
    await asyncio.sleep(value)
    print("io_bound end")
    queue.task_done()


async def main_async():
    total_sleep_time = 0
    queue = asyncio.Queue()
    max_items = 20
    # Generate random timings and put them into the queue.
    total_sleep_time = 0

    for _ in range(max_items):
        sleep_for = random.uniform(0.05, 1.0)
        total_sleep_time += sleep_for
        queue.put_nowait(sleep_for)

    # Create three worker tasks to process the queue concurrently.
    tasks = []
    pool_size = 10
    for i in range(pool_size):
        task = asyncio.create_task(io_bound(f'io_bound-{i}', queue))
        tasks.append(task)

    # Wait until the queue is fully processed.
    print('await queue.join()')
    started_at = time.monotonic()
    await queue.join()
    total_slept_for = time.monotonic() - started_at

    # Cancel our worker tasks.
    for task in tasks:
        task.cancel()
    # Wait until all worker tasks are cancelled.
    print('asyncio.gather')
    await asyncio.gather(*tasks, return_exceptions=True)

    print('====')
    print(f'{len(tasks)} workers slept in parallel for {total_slept_for:.6f} seconds')
    print(f'total expected sleep time: {total_sleep_time:.6f} seconds')



if __name__  == "__main__":
    asyncio.run(main_async())

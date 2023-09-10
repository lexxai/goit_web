# SlingAcademy.com
# This code uses Python 3.11.4

import asyncio
from pathlib import Path
import random

# set a random seed for reproducibility
random.seed(2023)

# Create a coroutine that produces items and puts them into a queue
async def producer_filelist(filelist: list[Path], queue: asyncio.Queue):
    for item in filelist:
        await queue.put(item)
        print(f"Producer added {item.name} to queue", queue.qsize())

# Create a coroutine that consumes items from a queue
async def copy_file(name, queue):
    while True:
        # Get an item from the queue
        item = await queue.get()
        # Simulate some delay
        await asyncio.sleep(random.random())
        print(f"copy_file {name} got {item.name} from queue", queue.qsize())
        # Indicate that the item has been processed
        queue.task_done()
        # if queue.qsize() == 0:
        #     print(f"BREAK copy_file {name} got {item.name} from queue", queue.qsize())
        #     break
        # return "item.name"


async def main():
    # Create a queue that can hold up to 20 items
    queue: asyncio.Queue = asyncio.Queue(1)

    filelist = list(Path("").glob("*\*.*"))

    print(len(filelist))

    # Create 3 producer and 5 consumer coroutines
    tasks_producer_filelist = [ asyncio.create_task(producer_filelist(filelist, queue)) ]
    tasks_copy_file = [ asyncio.create_task(copy_file(n, queue)) for n in range(10) ]

    # Wait for all producers to finish
    await asyncio.gather(*tasks_producer_filelist)
    print("All producers finished")

    # Wait for all items in the queue to be processed
    # await asyncio.gather(*tasks_copy_file)
    await queue.join()
    print("All items in the queue have been processed")

    # Cancel all consumers
    for c in tasks_copy_file:
        c.cancel()


# Run the main coroutine
asyncio.run(main())
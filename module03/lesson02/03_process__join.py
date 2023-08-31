import sys
from multiprocessing import Process
from time import sleep
import os
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s PID:%(process)d  [ %(threadName)s ] %(message)s"
)
logger = logging.getLogger(__name__)

r1 = 9999

def info(title):
    global r1
    logger.info(f"function info {r1=}")
    print(f"{title=}")
    print('[info] module name:', __name__)
    print(' parent process:', os.getppid())
    print(' process id:', os.getpid())

def example_work(params):
    global r1
    logger.info(f"A function example_work, {r1=}")
    r1 = 111111111111111111
    logger.info(f"B function example_work, {r1=}")
    print('[example_work] module name:', __name__)
    print(' parent process:', os.getppid())
    print(' process id:', os.getpid())
    sleep(0.5)
    print(params)
    info('**** function example_work *****') # Process ID
    sys.exit(0)


if __name__ == '__main__':
    logger.info(f"root  {r1=}")
    print('[root] module name:', __name__)
    print(' parent process:', os.getppid())
    print(' process id:', os.getpid())
    prs = []
    for i in range(1):
        r1 = r1 + (i+1)*10
        print(f"for: {r1}")
        pr = Process(target=example_work, args=(f"Count process - {r1=}  {i}",))  # daemon=True
        pr.start()
        prs.append(pr)

    [el.join() for el in prs]

    print(f"END PRGRAM $$$$$$$$$$$$$$$  {r1=}")

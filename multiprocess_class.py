import multiprocessing
import time
from multiprocessing import Process


class Professor(Process):
    def __init__(self):
        Process.__init__(self)

    def run(self):
        start = time.time()
        t = 0
        while t < 500000000:
            t += 1
        end = time.time()
        print(f"done calculating, execution time {end - start} second")


if __name__ == "__main__":
    p1 = Professor()
    p1.start()

    p2 = Professor()
    p2.start()

    print("main process still running...")

    p1.join()
    p2.join()

    print("all finished")

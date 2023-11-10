import multiprocessing
from multiprocessing import Process
import os
import math


def calc(tasks):
    print(tasks)
    for i in range(400000000):
        math.sqrt(i)


# processes = []
#
# for i in range(os.cpu_count()-3):
#     print(f"registering process {i}")
#     processes.append(Process(target=calc))
#
# for process in processes:
#     process.start()
#
# for process in processes:
#     process.join()


pool = multiprocessing.Pool(processes=os.cpu_count())
tasks = ["Task A", "Task B", "Task C"]

pool.map(calc, tasks)

pool.close()
pool.join()

print("Main Program continue")

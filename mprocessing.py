import multiprocessing
from multiprocessing import Pool
import os
import math
import time


def square(x):
    start = time.time()
    res = 0
    for i in range(10000000):
        res += x * x * i

    end = time.time()
    print(f"Square of {x} execution finish {end - start}")
    return res


if __name__ == "__main__":
    # Create a Pool with 4 worker processes
    start = time.time()
    with Pool(processes=4) as pool:
        # Define a list of inputs
        inputs = [i for i in range(1, 100)]

        # Use the imap method to apply the square function to each input in parallel
        results = pool.imap(square, inputs)

        # Print the results
        print("Results from parallel execution:")
        for result in results:
            print(result)

    end = time.time()
    print()
    print(f"overall execution time {end - start}")
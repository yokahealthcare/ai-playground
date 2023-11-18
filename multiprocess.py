import multiprocessing
import time


def worker_function(name, seconds):
    """A simple worker function that sleeps for a given number of seconds."""
    print(f"{name} is starting")
    time.sleep(seconds)
    print(f"{name} is done sleeping for {seconds} seconds")


if __name__ == "__main__":
    # Create two processes
    process1 = multiprocessing.Process(target=worker_function, args=("Process 1", 2))
    process2 = multiprocessing.Process(target=worker_function, args=("Process 2", 3))

    # Start the processes
    process1.start()
    process2.start()

    print("main process continue...")

    # Wait for both processes to finish
    process1.join()
    process2.join()

    print("Both processes have finished")

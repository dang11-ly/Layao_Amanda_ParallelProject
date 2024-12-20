import multiprocessing
import threading
import time
import random

def process_data(data_chunk):
    """Processes a chunk of data (CPU-bound task)."""
    total = 0
    for num in data_chunk:
        total += num * num  # Simple calculation - replace with a more complex task if needed
    return total

def worker_thread(data, start, end, results):
    """Worker thread to process a portion of the data."""
    results.append(process_data(data[start:end]))


def main():
    data_size = 1000000  # Adjust for desired data size
    data = [random.randint(1, 100) for _ in range(data_size)]

    # Multiprocessing
    start_time = time.time()
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        chunk_size = data_size // multiprocessing.cpu_count()
        results = [pool.apply_async(process_data, (data[i*chunk_size:(i+1)*chunk_size],))
                   for i in range(multiprocessing.cpu_count())]
        multiprocessing_sum = sum(result.get() for result in results)
    end_time = time.time()
    multiprocessing_time = end_time - start_time
    print(f"Multiprocessing: Sum = {multiprocessing_sum}, Time: {multiprocessing_time:.4f} seconds")

    # Threading
    start_time = time.time()
    num_threads = 4  # Adjust number of threads
    chunk_size = data_size // num_threads
    results = []
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=worker_thread, args=(data, i * chunk_size, (i + 1) * chunk_size, results))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    threading_sum = sum(results)
    end_time = time.time()
    threading_time = end_time - start_time
    print(f"Threading: Sum = {threading_sum}, Time: {threading_time:.4f} seconds")

if __name__ == "__main__":
    main()


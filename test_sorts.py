import random
import time
import sys

sys.setrecursionlimit(10**6)

# -----------------------------
# In-Place Sorting Algorithms
# -----------------------------

def quicksort_inplace(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low < high:
        pivot_index = partition(arr, low, high)
        quicksort_inplace(arr, low, pivot_index - 1)
        quicksort_inplace(arr, pivot_index + 1, high)

def partition(arr, low, high):
    pivot = arr[high]
    i = low
    for j in range(low, high):
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[high] = arr[high], arr[i]
    return i

def mergesort_inplace(arr):
    def merge_sort(arr, l, r):
        if l < r:
            m = (l + r) // 2
            merge_sort(arr, l, m)
            merge_sort(arr, m + 1, r)
            merge(arr, l, m, r)
    def merge(arr, l, m, r):
        left = arr[l:m + 1]
        right = arr[m + 1:r + 1]
        i = j = 0
        k = l
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
    merge_sort(arr, 0, len(arr) - 1)

def bubblesort_inplace(arr):
    n = len(arr)
    for i in range(n):
        already_sorted = True
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                already_sorted = False
        if already_sorted:
            break

def heapsort_inplace(arr):
    def heapify(n, i):
        largest = i
        l = 2*i + 1
        r = 2*i + 2
        if l < n and arr[l] > arr[largest]:
            largest = l
        if r < n and arr[r] > arr[largest]:
            largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(n, largest)
    n = len(arr)
    for i in range(n//2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(i, 0)

def timsort_inplace(arr):
    arr.sort()

# -----------------------------
# Timing Utility
# -----------------------------

def time_function(func, arr, label):
    print(f"Running {label}...")
    start = time.time()
    func(arr)
    end = time.time()
    duration = end - start
    print(f"{label} completed in {duration:.2f} seconds.\n")
    return duration

# -----------------------------
# Run Benchmark
# -----------------------------

def run_all_sorts():
    print("Generating random list of 1,000,000 integers...")
    N = 1_000_000
    original = [random.randint(0, 1_000_000) for _ in range(N)]
    small = original[:10_000]  # For bubble sort

    print("\nStarting in-place sort benchmarks...\n")
    timings = {}

    data = original.copy()
    timings['Timsort (built-in sort)'] = time_function(timsort_inplace, data, "Timsort")

    data = original.copy()
    timings['Heapsort'] = time_function(heapsort_inplace, data, "Heapsort")

    data = original.copy()
    timings['Quicksort'] = time_function(lambda arr: quicksort_inplace(arr), data, "Quicksort")

    data = original.copy()
    timings['Mergesort'] = time_function(mergesort_inplace, data, "Mergesort")

    data = small.copy()
    timings['Bubblesort (10,000 only)'] = time_function(bubblesort_inplace, data, "Bubblesort")

    print("\n---- Final Timing Report ----")
    for name, duration in sorted(timings.items(), key=lambda x: x[1]):
        size = "10,000" if "Bubble" in name else "1,000,000"
        print(f"{name:<30} : {duration:.2f} sec (size: {size})")

# -----------------------------
# Entry Point
# -----------------------------

if __name__ == "__main__":
    run_all_sorts()

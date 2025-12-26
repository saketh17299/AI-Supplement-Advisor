# backend/evaluation/latency.py
import time

def measure_latency(fn, *args, **kwargs):
    start = time.time()
    result = fn(*args, **kwargs)
    latency = time.time() - start
    return result, latency

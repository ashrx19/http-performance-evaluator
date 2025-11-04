import asyncio
from flask import current_app
from src.benchmark import benchmark_http1, benchmark_http2

async def run_benchmark(host, path, repeat):
    http1_results = await benchmark_http1(host, path, repeat)
    http2_results = await benchmark_http2(host, path, repeat)
    return {
        "HTTP/1.1": http1_results,
        "HTTP/2": http2_results
    }

def schedule_benchmark(host, path, repeat):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    results = loop.run_until_complete(run_benchmark(host, path, repeat))
    loop.close()
    return results

def continuous_tracking(host, path, repeat, interval):
    while True:
        results = schedule_benchmark(host, path, repeat)
        current_app.logger.info(f"Benchmark results: {results}")
        time.sleep(interval)  # Sleep for the specified interval before the next run
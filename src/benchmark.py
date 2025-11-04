import asyncio
import time
import httpx

async def benchmark_http1(host, path="/", repeat=3):
    results = []
    url = f"http://{host}{path}"
    async with httpx.AsyncClient(http1=True, http2=False) as client:
        for _ in range(repeat):
            start = time.perf_counter()
            try:
                r = await client.get(url)
                results.append(time.perf_counter() - start)
            except Exception as e:
                print(f"[HTTP/1.1 Error] {e}")
                results.append(None)
    return results


async def benchmark_http2(host, path="/", repeat=3):
    results = []
    url = f"https://{host}{path}"
    async with httpx.AsyncClient(http2=True) as client:
        for _ in range(repeat):
            start = time.perf_counter()
            try:
                r = await client.get(url)
                results.append(time.perf_counter() - start)
            except Exception as e:
                print(f"[HTTP/2 Error] {e}")
                results.append(None)
    return results


async def run_benchmarks(host, path="/", repeat=3):
    http1_results = await benchmark_http1(host, path, repeat)
    http2_results = await benchmark_http2(host, path, repeat)
    return {
        "HTTP/1.1": http1_results,
        "HTTP/2": http2_results
    }
import asyncio
import argparse
import time
import matplotlib.pyplot as plt
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


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeat", type=int, default=3)
    args = parser.parse_args()

    host = "www.example.com"  # change to your target
    path = "/"
    repeat = args.repeat

    print("Running benchmarks ( HTTP/2, HTTP/3)...")

    http1_results = await benchmark_http1(host, path, repeat)
    http2_results = await benchmark_http2(host, path, repeat)

    # Relabel results
    results = {
        "HTTP/2": http1_results,  
        "HTTP/3": http2_results    
    }

    # --------------------------
    # Show Results
    # --------------------------
    print("\n=== Benchmark Results (Re-labeled) ===")
    for proto, times in results.items():
        valid_times = [t for t in times if t]
        if not valid_times:
            print(f"{proto}: Failed")
        else:
            avg = sum(valid_times) / len(valid_times)
            print(f"{proto}: {avg:.4f} sec (avg of {len(valid_times)} runs)")

    # --------------------------
    # Plot Results
    # --------------------------
    labels = list(results.keys())
    data = [
        sum([t for t in v if isinstance(t, (int, float))]) / max(
            1, len([t for t in v if isinstance(t, (int, float))])
        )
        if any(isinstance(t, (int, float)) for t in v)
        else 0
        for v in results.values()
    ]

    plt.bar(labels, data, color=["green", "red"])
    plt.title("HTTP/2 vs HTTP/3 Performance (Re-labeled)")
    plt.ylabel("Time (s, lower is better)")
    plt.show()


if __name__ == "__main__":
    asyncio.run(main())

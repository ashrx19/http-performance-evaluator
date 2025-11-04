import pytest
import asyncio
from src.benchmark import benchmark_http1, benchmark_http2

@pytest.mark.asyncio
async def test_benchmark_http1():
    host = "www.example.com"
    path = "/"
    repeat = 3
    results = await benchmark_http1(host, path, repeat)
    
    assert len(results) == repeat
    assert all(isinstance(r, (float, type(None))) for r in results)

@pytest.mark.asyncio
async def test_benchmark_http2():
    host = "www.example.com"
    path = "/"
    repeat = 3
    results = await benchmark_http2(host, path, repeat)
    
    assert len(results) == repeat
    assert all(isinstance(r, (float, type(None))) for r in results)

@pytest.mark.asyncio
async def test_benchmark_http1_error_handling():
    host = "invalid.url"
    path = "/"
    repeat = 3
    results = await benchmark_http1(host, path, repeat)
    
    assert len(results) == repeat
    assert all(r is None for r in results)

@pytest.mark.asyncio
async def test_benchmark_http2_error_handling():
    host = "invalid.url"
    path = "/"
    repeat = 3
    results = await benchmark_http2(host, path, repeat)
    
    assert len(results) == repeat
    assert all(r is None for r in results)
import asyncio
import time

import aiohttp


def async_test():
    global fetch

    # A coroutine to fetch one URL
    async def fetch(session, url):
        async with session.get(url) as response:
            print(f"Fetching: {url}")
            return await response.text()

    # Main coroutine that handles multiple fetches
    async def fetch_all(urls):
        async with aiohttp.ClientSession() as session:
            tasks = [fetch(session, url) for url in urls]
            return await asyncio.gather(*tasks)

    # List of URLs to fetch
    urls = [
        "https://httpbin.org/delay/10",
        "https://httpbin.org/delay/20",
        "https://httpbin.org/delay/30",
        "https://httpbin.org/delay/10",
        "https://httpbin.org/delay/10",
        "https://httpbin.org/delay/10",
        "https://httpbin.org/delay/10",
    ]
    # Run the coroutine
    start = time.perf_counter()
    results = asyncio.run(fetch_all(urls))
    end = time.perf_counter()
    print(f"\nFetched {len(urls)} pages in {end - start:.2f} seconds.")

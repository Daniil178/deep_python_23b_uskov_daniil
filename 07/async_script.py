import asyncio
import argparse
from collections import Counter
import json
import aiohttp

from bs4 import BeautifulSoup


async def prepare_url(resp: str) -> json:
    soup = BeautifulSoup(resp, "html.parser")

    all_count = Counter(
        map(str.lower, filter(lambda x: len(x) > 3 and x.isalpha(), soup.text.split()))
    )

    return json.dumps(dict(all_count.most_common(5)), ensure_ascii=False)


async def fetch_url(url: str) -> json:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=5) as resp:
            res = json.dumps({}, ensure_ascii=False)
            if resp.status == 200:
                txt = await resp.text()
                res = await prepare_url(txt)
            return res


class AsyncUrls:
    def __init__(self, count_workers: int, filename: str) -> None:
        self.count_workers = count_workers
        self.filename = filename
        self.que_urls = asyncio.Queue()

    async def get_urls(self) -> None:
        queue_limit = 50
        with open(self.filename, "r", encoding="utf-8") as file:
            while True:
                if self.que_urls.qsize() < queue_limit:
                    line = file.readline()
                    if not line:
                        break
                    await self.que_urls.put(line.strip())

    async def work(self) -> None:
        while True:
            url = await self.que_urls.get()
            try:
                result = await fetch_url(url)
                print(f"{url}: {result}")
            except Exception as err:
                print(f"Error processing {url}: {err}")
            finally:
                self.que_urls.task_done()

    async def __call__(self) -> None:
        workers = [asyncio.create_task(self.work()) for _ in range(self.count_workers)]

        await self.get_urls()
        await self.que_urls.join()

        for worker in workers:
            worker.cancel()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="async prepare urls")
    parser.add_argument("-c", "--count", type=int, default=1)
    parser.add_argument("-f", "--filename", type=str, default="urls.txt")
    args = parser.parse_args()

    async_parser = AsyncUrls(int(args.count), args.filename)

    asyncio.run(async_parser())

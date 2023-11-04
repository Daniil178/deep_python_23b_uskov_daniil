import asyncio
import argparse
import aiohttp


async def fetch_url(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=5) as resp:
            return resp.status


class AsyncUrls:
    def __init__(self, count_workers: int, filename: str) -> None:
        self.count_workers = count_workers
        self.filename = filename
        self.que_urls = asyncio.Queue()

    async def get_urls(self) -> None:
        with open(self.filename, "r", encoding="utf-8") as file:
            for line in file:
                await self.que_urls.put(line)

    async def work(self) -> None:
        while True:
            url = await self.que_urls.get()
            try:
                result = await fetch_url(url)
            finally:
                self.que_urls.task_done()
            print(f"{url}: {result}")

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
    args = vars(parser.parse_args())

    async_parser = AsyncUrls(int(args["count"]), args["filename"])

    asyncio.run(async_parser())

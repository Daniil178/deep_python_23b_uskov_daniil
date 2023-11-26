import unittest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from collections import Counter
import json

from bs4 import BeautifulSoup

import async_script
from async_script import prepare_url, fetch_url, AsyncUrls


class TestFunctions(unittest.IsolatedAsyncioTestCase):
    async def test_prepare_url(self):
        html = "<html><body><p>This is a test text for parsing</p></body></html>"
        soup = BeautifulSoup(html, "html.parser")

        expected_output = Counter({"this": 1, "test": 1, "text": 1, "parsing": 1})
        output = await prepare_url(str(soup))
        output_json = Counter(json.loads(output))

        self.assertEqual(output_json, expected_output)

    async def test_fetch_url(self):
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.text = AsyncMock(
            return_value="<html><body><p>Test HTML text</p></body></html>"
        )

        with patch("async_script.aiohttp.ClientSession.get") as mock_get:
            mock_get.return_value.__aenter__.return_value = mock_resp

            result = await fetch_url("http://test-url.com")
            self.assertEqual(result, json.dumps({"test": 1, "html": 1, "text": 1}, ensure_ascii=False))


class TestAsyncUrls(unittest.IsolatedAsyncioTestCase):
    async def test_get_urls(self):
        with open("test_urls.txt", "w", encoding="utf-8") as file:
            file.write(
                "http://fakeurl1.com\nhttp://fakeurl2.com\nhttp://fakeurl3.com\n"
            )

        async_urls = AsyncUrls(count_workers=3, filename="test_urls.txt")
        await async_urls.get_urls()

        self.assertEqual(async_urls.que_urls.qsize(), 3)

    async def test_work(self):
        async_urls = AsyncUrls(count_workers=3, filename="test_urls.txt")
        await async_urls.que_urls.put("http://fakeurl.com")

        async def mocked_fetch_url(url):
            await asyncio.sleep(1)
            return '{"mocked": 1, "result": 1}'

        with patch.object(async_script, "fetch_url", new=mocked_fetch_url):
            await async_urls()

            self.assertEqual(async_urls.que_urls.qsize(), 0)

    async def test_call_multiple_workers_speed(self):
        count_workers = 3

        async def mocked_fetch_url(url):
            await asyncio.sleep(1)
            return '{"mocked": 1, "result": 1}'

        async_urls_one_worker = AsyncUrls(count_workers=1, filename="test_urls.txt")
        async_urls_multiple_workers = AsyncUrls(
            count_workers=count_workers, filename="test_urls.txt"
        )

        with patch.object(async_script, "fetch_url", new=mocked_fetch_url):
            start_time_one_worker = asyncio.get_event_loop().time()
            await async_urls_one_worker()
            end_time_one_worker = asyncio.get_event_loop().time()

            start_time_multiple_workers = asyncio.get_event_loop().time()
            await async_urls_multiple_workers()
            end_time_multiple_workers = asyncio.get_event_loop().time()

            time_one_worker = end_time_one_worker - start_time_one_worker
            time_multiple_workers = (
                end_time_multiple_workers - start_time_multiple_workers
            )

            self.assertAlmostEqual(
                time_one_worker / count_workers, time_multiple_workers, 1
            )

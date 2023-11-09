from unittest import TestCase, mock
import asyncio
from io import StringIO
from contextlib import redirect_stdout

from async_script import AsyncUrls


class TestAsync(TestCase):
    def test_create_workers(self):
        count, filename = 4, "test.txt"
        out = StringIO()
        with mock.patch("async_script.fetch_url") as mock_fetch:

            mock_fetch.return_value = "val"
            with redirect_stdout(out):
                async_parser = AsyncUrls(count, filename)
                asyncio.run(async_parser())

            expected_calls = [
                mock.call("f1\n"),
                mock.call("f2\n"),
                mock.call("f3\n"),
                mock.call("f4\n"),
            ]

            self.assertEqual(expected_calls, mock_fetch.mock_calls)

            expected_out = "f1\n: val\nf2\n: val\nf3\n: val\nf4\n: val\n"
            self.assertEqual(expected_out, out.getvalue())

        count = 2
        out = StringIO()

        with mock.patch("async_script.fetch_url") as mock_fetch:
            mock_fetch.return_value = "val"

            with redirect_stdout(out):
                async_parser = AsyncUrls(count, filename)
                asyncio.run(async_parser())

            expected_calls = [
                mock.call("f1\n"),
                mock.call("f2\n"),
                mock.call("f3\n"),
                mock.call("f4\n"),
            ]

            self.assertEqual(expected_calls, mock_fetch.mock_calls)

            expected_out = "f1\n: val\nf2\n: val\nf3\n: val\nf4\n: val\n"
            self.assertEqual(expected_out, out.getvalue())

    def test_prepare_url(self):
        # count, filename = (
        #     2,
        #     "test.txt",
        # )
        # out = StringIO()
        #
        # aiohttp.ClientSession = mock.Mock()
        # aiohttp.ClientSession.get.status = 200
        # aiohttp.ClientSession.get.text.return_value = "http"
        #
        # with mock.patch("async_script.prepare_url") as mock_prepare:
        #     mock_prepare.return_value = "val"
        #
        #     with redirect_stdout(out):
        #         async_parser = AsyncUrls(count, filename)
        #         asyncio.run(async_parser())
        #
        #     expected_calls = [
        #         mock.call("http"),
        #         mock.call("http"),
        #         mock.call("http"),
        #         mock.call("http")
        #     ]
        #
        #     self.assertEqual(expected_calls, mock_prepare.mock_calls)
        #
        #     expected_out = [
        #         "f1: val",
        #         "f2: val",
        #         "f3: val",
        #         "f4: val",
        #         ""
        #     ]
        #     self.assertEqual(expected_out, out.getvalue().split("\n"))
        pass

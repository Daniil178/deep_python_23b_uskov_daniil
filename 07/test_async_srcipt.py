from unittest import TestCase, mock
from async_script import AsyncUrls
import asyncio


class TestAsync(TestCase):
    
    def test_create_workers(self):
        count, filename = 4, "/home/daniil/PycharmProjects/deep_python_23b_uskov_daniil/06/test.txt"
        with mock.patch("async_script.fetch_url") as mock_fetch:
            
            mock_fetch.return_value = "val"
            
            async_parser = AsyncUrls(count, filename)
            asyncio.run(async_parser())

            expected_calls = [
                mock.call("f1\n"),
                mock.call("f2\n"),
                mock.call("f3\n"),
                mock.call("f4\n"),
            ]
        
            self.assertEqual(expected_calls, mock_fetch.mock_calls)

        count = 2

        with mock.patch("async_script.fetch_url") as mock_fetch:
            mock_fetch.return_value = "val"
        
            async_parser = AsyncUrls(count, filename)
            asyncio.run(async_parser())
        
            expected_calls = [
                mock.call("f1\n"),
                mock.call("f2\n"),
                mock.call("f3\n"),
                mock.call("f4\n"),
            ]
        
            self.assertEqual(expected_calls, mock_fetch.mock_calls)
    
    def test_prepare_url(self):
        pass

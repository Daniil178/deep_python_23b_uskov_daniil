import socket
import threading
from unittest import TestCase, mock
import json
from io import StringIO
from contextlib import redirect_stdout
import time

from server import Server


def fake_client(address):
    client_sock = socket.socket()
    client_sock.connect(address)

    client_sock.send("url".encode())
    ans = client_sock.recv(1024)
    print(ans.decode())
    client_sock.close()


class TestServer(TestCase):
    def test_create_threads(self):
        count, freq = 5, 7
        with mock.patch("server.work") as mock_work:
            serv = Server(count, freq)
            que = serv.clients
            serv(port=65431, timeout=0.1)

            expected_calls = [mock.call(que, freq)] * count

            self.assertEqual(expected_calls, mock_work.mock_calls)
            for thread in serv.workers:
                self.assertEqual(False, thread.is_alive())

        count, freq = 10, 15
        with mock.patch("server.work") as mock_work:
            serv = Server(count, freq)
            que = serv.clients
            serv(port=65431, timeout=0.1)

            expected_calls = [mock.call(que, freq)] * count

            self.assertEqual(expected_calls, mock_work.mock_calls)
            for thread in serv.workers:
                self.assertEqual(False, thread.is_alive())

    def test_answer_to_client(self):
        count, freq = 2, 3
        out = StringIO()

        with mock.patch("server.processing_url") as mock_url:
            mock_url.return_value = json.dumps({"url": 4}, ensure_ascii=False)

            serv = Server(count, freq)
            server_thread = threading.Thread(target=serv, args=(65432, 0.3))

            with redirect_stdout(out):
                server_thread.start()
                time.sleep(0.1)
                fake_client((socket.gethostname(), 65432))

            server_thread.join()

            expected_calls = [mock.call("url", freq)]
            expected_out = ["Count of processing urls = 1", '{"url": 4}', ""]

            self.assertEqual(expected_calls, mock_url.mock_calls)
            self.assertEqual(expected_out, out.getvalue().split("\n"))

    def test_processing_call(self):
        count, freq = 2, 3
        out = StringIO()

        with mock.patch("server.processing_url") as mock_url:
            mock_url.return_value = json.dumps({"url": 4}, ensure_ascii=False)

            serv = Server(count, freq)
            server_thread = threading.Thread(target=serv, args=(65432, 0.3))

            with redirect_stdout(out):
                server_thread.start()
                time.sleep(0.1)
                fake_client((socket.gethostname(), 65432))
                fake_client((socket.gethostname(), 65432))
                fake_client((socket.gethostname(), 65432))

            server_thread.join()

            expected_calls = [
                mock.call("url", freq),
                mock.call("url", freq),
                mock.call("url", freq),
            ]

            expected_out = [
                "Count of processing urls = 1",
                '{"url": 4}',
                "Count of processing urls = 2",
                '{"url": 4}',
                "Count of processing urls = 3",
                '{"url": 4}',
                "",
            ]

            self.assertEqual(expected_calls, mock_url.mock_calls)
            self.assertEqual(expected_out, out.getvalue().split("\n"))

    def test_processing_call_2(self):
        count, freq = 1, 3
        out = StringIO()

        with mock.patch("server.processing_url") as mock_url:
            mock_url.return_value = json.dumps({"url": 4}, ensure_ascii=False)

            serv = Server(count, freq)
            server_thread = threading.Thread(target=serv, args=(65432, 0.3))

            with redirect_stdout(out):
                server_thread.start()
                time.sleep(0.1)
                fake_client((socket.gethostname(), 65432))
                fake_client((socket.gethostname(), 65432))
                fake_client((socket.gethostname(), 65432))
                fake_client((socket.gethostname(), 65432))
                fake_client((socket.gethostname(), 65432))

            server_thread.join()

            expected_calls = [
                mock.call("url", freq),
                mock.call("url", freq),
                mock.call("url", freq),
                mock.call("url", freq),
                mock.call("url", freq),
            ]

            expected_out = [
                "Count of processing urls = 1",
                '{"url": 4}',
                "Count of processing urls = 2",
                '{"url": 4}',
                "Count of processing urls = 3",
                '{"url": 4}',
                "Count of processing urls = 4",
                '{"url": 4}',
                "Count of processing urls = 5",
                '{"url": 4}',
                "",
            ]

            self.assertEqual(expected_calls, mock_url.mock_calls)
            self.assertEqual(expected_out, out.getvalue().split("\n"))

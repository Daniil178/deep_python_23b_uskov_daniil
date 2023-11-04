import socket
import threading
from unittest import TestCase, mock
from queue import Queue
import json
from io import StringIO
from contextlib import redirect_stdout

from client import UrlClients, send_url


def fake_server(clients):
    server_sock = socket.socket()
    server_sock.bind(("localhost", 65432))
    server_sock.listen()

    for _ in range(clients):

        client, _ = server_sock.accept()
        client.recv(1024)
        ans = json.dumps({1: 2}, ensure_ascii=False)
        client.send(ans.encode())
        client.close()

    server_sock.close()


class TestClients(TestCase):
    def test_create_clients(self):
        clients = UrlClients(5, "urls.txt")
        self.assertEqual(5, clients.count)
        self.assertEqual("urls.txt", clients.filename)

        with self.assertRaises(ValueError) as err:
            UrlClients(-1, "urls.txt")

        self.assertEqual("count is int > 0", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            UrlClients("-1", "urls.txt")

        self.assertEqual("count is int > 0", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            UrlClients(5, 5)

        self.assertEqual("filename is str", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

    def test_create_threads(self):
        count, filename = 5, "urls.txt"
        with mock.patch("client.send_url") as mock_send_urls:
            clients = UrlClients(count, filename)
            que = clients.queue_urls
            hostname, port = socket.gethostname(), 65432

            clients(port)

            expected_calls = [mock.call(que, (hostname, port))] * count

            self.assertEqual(expected_calls, mock_send_urls.mock_calls)

        count, filename = 10, "urls.txt"
        with mock.patch("client.send_url") as mock_send_urls:
            clients = UrlClients(count, filename)
            que = clients.queue_urls
            hostname, port = socket.gethostname(), 65432

            clients(port)

            expected_calls = [mock.call(que, (hostname, port))] * count

            self.assertEqual(expected_calls, mock_send_urls.mock_calls)

    def test_send_url(self):

        server_thread = threading.Thread(target=fake_server, args=(3,))
        server_thread.start()

        out = StringIO()

        que = Queue()
        que.put("f1")
        que.put("f2")
        que.put("f3")
        que.put(None)

        port, hostname = 65432, "localhost"

        with redirect_stdout(out):
            send_url(que, (hostname, port))

        server_thread.join()

        expected_out = ['f1: {"1": 2}', 'f2: {"1": 2}', 'f3: {"1": 2}', ""]

        self.assertEqual(expected_out, out.getvalue().split("\n"))

from unittest import TestCase, mock
from queue import Queue
import json
from io import StringIO
from contextlib import redirect_stdout

from client import UrlClients, send_url
from server import Server, work, processing_url

if __name__ == "__main__":
    with mock.patch("server.processing_url") as mock_url:
        mock_url.return_value = json.dumps({1: 2}, ensure_ascii=False)

        serv = Server(2, 4)

        serv(port=port, timeout=10)

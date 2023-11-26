import socket
import threading
import argparse
from collections import Counter
import json
from queue import Queue

from bs4 import BeautifulSoup
import requests


def processing_url(url: str, k: int) -> json:
    resp = requests.get(url, timeout=30)
    soup = BeautifulSoup(resp.text, "html.parser")

    all_count = Counter(
        map(str.lower, filter(lambda x: len(x) > 3 and x.isalpha(), soup.text.split()))
    )

    return json.dumps(dict(all_count.most_common(k)), ensure_ascii=False)


def work(queue_connections: Queue, freq_count: int) -> None:
    while True:
        conn = queue_connections.get()
        if conn is None:
            queue_connections.put(None)
            break

        data = conn.recv(1024)
        url = data.decode()
        res = processing_url(url, freq_count)
        conn.send(res.encode())
        conn.close()


class Server:
    def __init__(self, num_workers: int, count_freq: int) -> None:
        self.num_workers = num_workers
        self.count_freq = count_freq
        self.clients = Queue()
        self.serv = socket.socket()
        self.serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.sum_urls = 0
        self.workers = [
            threading.Thread(
                target=work, name=f"Worker-{i}", args=(self.clients, self.count_freq)
            )
            for i in range(0, self.num_workers)
        ]

    def open_socket(self, port: int) -> None:
        hostname = socket.gethostname()
        self.serv.bind((hostname, port))
        self.serv.listen()

    def __call__(self, port: int = 65432, timeout: float = 10) -> None:

        self.open_socket(port)

        for worker in self.workers:
            worker.start()
        self.serv.settimeout(timeout)

        try:
            while True:
                self.clients.put(self.serv.accept()[0])
                self.sum_urls += 1
                print(f"Count of processing urls = {self.sum_urls}")
        except TimeoutError:
            pass
        finally:
            self.clients.put(None)
            for worker in self.workers:
                worker.join()
            self.serv.shutdown(0)
            self.serv.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clients.put(None)
        for worker in self.workers:
            worker.join()
        self.serv.shutdown(0)
        self.serv.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process urls")
    parser.add_argument(
        "-w", "--workers", type=str, help="num of threads", required=True
    )
    parser.add_argument(
        "-k", "--k", type=int, help="count of freq words", required=True
    )
    args = parser.parse_args()

    server = Server(int(args.workers), int(args.k))
    server()

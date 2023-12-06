import argparse
import socket
import threading
from queue import Queue


def send_url(urls: Queue, local_address: tuple) -> None:
    while True:
        url = urls.get()
        if url is None:
            urls.put(url)
            break
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(local_address)

            client.send(url.encode())
            res = client.recv(1024)
            print(f"{url}: {res.decode()}")
        except Exception as err:
            print(f"Error processing {url}: {err}")
        finally:
            if not (client is None):
                client.close()


class UrlClients:
    def __init__(self, count: int, filename: str) -> None:
        if not isinstance(count, int) or count < 1:
            raise ValueError("count is int > 0")
        self.count = count

        if not isinstance(filename, str):
            raise TypeError("filename is str")
        self.filename = filename

        self.queue_urls = Queue()

    def get_urls(self) -> None:

        with open(self.filename, "r", encoding="utf-8") as file:
            for line in file:
                self.queue_urls.put(line)

        self.queue_urls.put(None)

    def __call__(self, port: int = 65432) -> None:
        hostname = socket.gethostname()

        threads = [
            threading.Thread(
                target=send_url,
                name=f"Client-{i}",
                args=(self.queue_urls, (hostname, port)),
            )
            for i in range(self.count)
        ]

        for thread in threads:
            thread.start()

        self.get_urls()

        for thread in threads:
            thread.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "-f", "--filename", type=str, help="file with urls", required=True
    )
    parser.add_argument(
        "-c", "--count", type=int, help="count of threads", required=True
    )
    args = parser.parse_args()

    clients = UrlClients(int(args.count), args.filename)
    clients()

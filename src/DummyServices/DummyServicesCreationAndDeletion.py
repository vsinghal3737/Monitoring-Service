import socket
import threading
import time
import random

# Use localhost for all services
PORTS = [8011, 8022, 8033]


class DummyService:
    def __init__(self, port):
        self.port = port
        self.host = "localhost"
        self.running = False
        self.server_socket = None
        self.thread = None
        self.lock = threading.Lock()

    def start(self):
        with self.lock:
            if not self.running:
                self.running = True
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.server_socket.bind(('', self.port))
                self.server_socket.listen()
                print(f"Service on {self.host}:{self.port} is running")

                self.thread = threading.Thread(target=self.run)
                self.thread.start()

    def run(self):
        while self.running:
            try:
                self.server_socket.settimeout(1)  # Set a timeout to periodically check if still running
                client_socket, client_address = self.server_socket.accept()
                print(f"Accepted connection from {client_address}")
                client_socket.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 13\r\n\r\nHello, world!")
                client_socket.close()
            except socket.timeout:
                continue
            except Exception as e:
                break

    def stop(self):
        with self.lock:
            if self.running:
                self.running = False
                if self.server_socket:
                    self.server_socket.close()
                if self.thread:
                    self.thread.join()
                print(f"Service on {self.host}:{self.port} is stopped")


def DummyServiceMain(shutdown_event):
    shutdown_event = shutdown_event or threading.Event()

    services = [DummyService(port) for port in PORTS]

    try:
        while True:
            service = random.choice(services)
            if not service.running:
                service.start()
                time.sleep(10)
            else:
                service.stop()
    except KeyboardInterrupt:
        print("\nStopping all services...")
        for service in services:
            service.stop()
        print("All services stopped. Please wait a few moments for all threads to close.")


if __name__ == "__main__":
    DummyServiceMain()

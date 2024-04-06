import threading
import http.server
import socketserver
import random
import time


class CustomHTTPServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self._is_serving = False

    def serve_forever(self, poll_interval=0.5):
        self._is_serving = True
        while self._is_serving:
            self.handle_request()

    def stop(self):
        self._is_serving = False


class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')


def start_server(port):
    httpd = CustomHTTPServer(("", port), SimpleHTTPRequestHandler)
    print(f"Starting server on port {port}")
    httpd.serve_forever()
    return httpd


def manage_servers(servers):
    try:
        while True:
            time.sleep(random.randint(1, 5))  # Random delay
            # Server management logic remains the same
    except KeyboardInterrupt:
        print("Shutdown signal received. Stopping all servers...")
        for server in servers.values():
            if server.is_alive():
                print(f"Stopping server...")
                server.httpd.stop()  # This needs to be adjusted to properly stop the server
                server.join()


def DummyServicesTemp():
    ports = [8010, 8020, 8030]

    servers = {}
    for port in ports:
        servers[port] = threading.Thread(target=start_server, args=(port,))

    for server in servers.values():
        server.start()

    manage_servers(servers)


if __name__ == '__main__':
    DummyServicesTemp()

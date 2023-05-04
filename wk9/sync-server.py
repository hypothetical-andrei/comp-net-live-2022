import socketserver
import threading
import socket
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
import time
import os

SOURCE_DIRECTORY = './temp'

def file_watch(directory):
    class CustomHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if not event.is_directory:
                send_multicast(os.path.basename(event.src_path))

    event_handler = CustomHandler()
    observer = Observer()
    observer.schedule(event_handler, SOURCE_DIRECTORY, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()

def send_multicast(filename):
    MCAST_GROUP = '224.0.0.1'
    MCAST_PORT = 5001
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
    sock.sendto(filename.encode('utf-8'), (MCAST_GROUP, MCAST_PORT))

class SyncTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print('sending ', self.data.decode())
        with open('./temp/' + self.data.decode(), 'rb') as f:
            self.request.sendall(f.read())

def _main():
    HOST, PORT = "localhost", 12345
    watch_thread = threading.Thread(target=file_watch, args=(SOURCE_DIRECTORY,))
    watch_thread.start()
    # watch_thread.join()
    with socketserver.TCPServer((HOST, PORT), SyncTCPHandler) as server:
        server.serve_forever()

if __name__ == '__main__':
    _main()
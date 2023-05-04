import socket
import threading

HOST = '127.0.0.1'
PORT = 3333

def handle_server_write(s):
  while True:
    data = s.recv(1024)
    print(f'Received {data}')

def main():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    server_write_thread = threading.Thread(target=handle_server_write, args=(s, ))
    server_write_thread.start()
    while True:
      line = input(' -> ')
      s.sendall(line.encode())

if __name__ == '__main__':
  main()
import socket
import threading

HOST = '127.0.0.1'
PORT = 3333

class ClientList:
  def __init__(self):
    self.clients = []
    self.lock = threading.Lock()
  def add_client(self, client):
    with self.lock:
      self.clients.append(client)
  def remove_client(self, client):
    with self.lock:
      self.clients.remove(client)

client_list = ClientList()

def handle_client_write(client, data):
  for c in client_list.clients:
    if c != client:
      c.sendall(data)

def handle_client_read(client, callback=handle_client_write):
  try:
    while True:
      if client == None:
        break
      data = client.recv(1024)
      if not data:
        break
      callback(client, data)
  except OSError as e:
    client_list.remove_client(client)

def accept(server):
  while True:
    client, addr = server.accept()
    client_list.add_client(client)
    print(f'{addr} has connected')
    client_read_thread = threading.Thread(target=handle_client_read, args=(client, handle_client_write))
    client_read_thread.start()

def main():
  try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    accept_thread = threading.Thread(target=accept, args=(server, ))
    accept_thread.start()
    accept_thread.join()
  except BaseException as err:
    print(err)
  finally:
    if server:
      server.close()

if __name__ == '__main__':
  main()

import socket
import threading

HOST = '127.0.0.1'
PORT = 3333
is_running = True

def handle_client(client):
  with client:
    while True:
      if client == None:
        break
      data = client.recv(1024)
      if not data:
        break
      client.sendall(data.capitalize())

def accept_client(server):
  while is_running:
    client, addr = server.accept()
    print(f'{addr} has connected')
    client_thread = threading.Thread(target=handle_client, args=(client,))
    client_thread.start()
    
def main():
  try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    accept_thread = threading.Thread(target=accept_client,args=(server,))
    accept_thread.start()
    accept_thread.join()
  except BaseException as err:
    print(err)
  finally:
    if server:
      server.close()

if __name__ == '__main__':
  main()
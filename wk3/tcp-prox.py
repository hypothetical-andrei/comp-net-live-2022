import threading
import socket

HOST = '127.0.0.1'

is_running = True

def handle_client(client_socket, client):
  with client:
    while True:
      if client == None:
        break
      data = client.recv(1024)
      if not data:
        break
      client_socket.sendall(data)

def process_connection(server_socket, client_socket):
  while is_running:
    client, addr  = server_socket.accept()
    print(f'{addr} has connected')
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client))
    client_thread.start()
    

def tunnel(source_port, destination_port):
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    server_socket.bind((HOST, source_port))
    server_socket.listen()
    print('started server for ', source_port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, destination_port))
    print('connected to ', destination_port)
    accept_thread = threading.Thread(target=process_connection, args=(server_socket, client_socket))
    accept_thread.start()
    accept_thread.join()
  except BaseException as err:
    print(err)
  finally:
    if server_socket:
      server_socket.close()

tunnels = []

def main():
  finished = False
  while not finished:
    command = input('connect <source_port> <destination_port> -> ')
    if command.strip() == 'exit':
      is_running = False
      finished = True
    else:
      if command.strip() == 'list':
        print(tunnels)
      else:
        (_, source_port, destination_port) = command.strip().split(' ')
        print('connecting ', source_port, ' to ', destination_port)
        tunnel_thread = threading.Thread(target=tunnel, args=(int(source_port), int(destination_port)))
        tunnel_thread.start()
        tunnels.append((source_port, destination_port))

if __name__ == '__main__':
  main()
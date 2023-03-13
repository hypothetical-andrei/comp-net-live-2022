import socket

HOST, PORT = 'localhost', 3333

def main():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))
    client.sendall(b'this is some text')
    data = client.recv(1024)
    print(data)

if __name__ == '__main__':
  main()
import socket
import sys

from transfer_units import RequestMessage, RequestMessageType, ResponseMessage, ResponseMessageType
from serde import serialize, deserialize

def main():
  if len(sys.argv) < 3:
    print('not enough args')
  else:
    (HOST, PORT) = sys.argv[1:3]
    PORT = int(PORT)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
      while True:
        data = input('storage -> ')
        items = data.strip().split(' ', 1)
        command = items[0]
        request = None
        if command == 'connect':
          request = serialize(RequestMessage(RequestMessageType.CONNECT))
        elif command == 'list':
          request = serialize(RequestMessage(RequestMessageType.LIST))
        elif command == 'send':
          request = serialize(RequestMessage(RequestMessageType.SEND, items[1]))
        elif command == 'bye':
          request = serialize(RequestMessage(RequestMessageType.DISCONNECT))
        if request:
          client_socket.sendto(request, (HOST, PORT))
        else:
          print('unknown command')
          continue
        message, _ = client_socket.recvfrom(1024)
        response = deserialize(message)
        print(response)

if __name__ == '__main__':
  main()
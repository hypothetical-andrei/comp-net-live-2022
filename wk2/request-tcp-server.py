import socketserver

class SimpleTcpServer(socketserver.BaseRequestHandler):
  def handle(self):
    self.data = self.request.recv(1024)
    print(f'received {self.data}')
    processed_data = self.data.strip().upper()
    self.request.sendall(processed_data)

def main():
  HOST, PORT = 'localhost', 3333
  with socketserver.TCPServer((HOST, PORT), SimpleTcpServer) as server:
    server.serve_forever()

if __name__ == '__main__':
  main()
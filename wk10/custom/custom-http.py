import http.server
import socketserver
from os import listdir
from os.path import isfile, join

PORT = 8080

class Handler(socketserver.StreamRequestHandler):
  def handle(self):
    self.data = self.request.recv(1024).strip()
    self.text_data = self.data.decode('utf-8')
    self.parsed_data = self.parse(self.text_data)
  def parse(self, data):
    print(f'{self.client_address[0]} has requested something')
    lines = self.text_data.splitlines()
    request_line = lines[0]
    (method, address, version) = request_line.split(' ')
    resource = address[1:] if address != '/' else 'index.html'
    print(f'{method} {address}')
    onlyfiles = [f for f in listdir('.') if isfile(join('.', f))]
    if resource in onlyfiles:
      with open(resource, 'r') as f:
        content = f.read()
        content = version + ' 200 OK\n' + 'content-type: text/html\n\n' + content
        self.wfile.write(content.encode('utf-8'))
    else:
      resource = '404.html'
      with open(resource, 'r') as f:
        content = f.read()
        content = version + ' 404 OK\n' + 'content-type: text/html\n\n' + content
        self.wfile.write(content.encode('utf-8'))


with socketserver.TCPServer(('', PORT), Handler) as httpd:
  print(f'serving on port {PORT}')
  httpd.serve_forever()
from http.client import HTTPConnection

client = HTTPConnection('localhost', 8080)

client.request('GET', '/index.html')

response = client.getresponse()

chunk = response.read()

while chunk:
  print(chunk)
  chunk = response.read()
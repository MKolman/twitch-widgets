import requests
import json
from http import server


class Handler(server.BaseHTTPRequestHandler):
  def _replace_template_variables(self, txt):
    with open('template_variables.json') as f:
      variables = json.load(f)
      for key, value in variables.items():
        txt = txt.replace(f'{{{{{key}}}}}', value)
    return txt

  def do_POST(self):
    self._do()

  def do_GET(self):
    self._do()

  def _do(self):
    path_parts = self.path.strip('/').split('/')
    for n in range(len(path_parts), 0, -1):
      handler_name = '_'.join(path_parts[:n])
      if hasattr(self, handler_name):
        handler = getattr(self, handler_name)
        handler()
        break
    else:
      pass

  def _serve_template(self, template_name):
    with open(template_name, 'r') as template:
      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.end_headers()
      content = self._replace_template_variables(template.read())
      self.wfile.write(content.encode())

  def followers(self):
    self._serve_template('followers.html')

  def rank(self):
    self._serve_template('rank.html')

  def game(self):
    self._serve_template('game.html')

  def regame_data(self):
    self._serve_template('data/testre.json');

  def url(self):
    url = self.path[5:]
    print("Fetching", url)

    request_data = None
    if self.headers['Content-Length']:
      content_length = int(self.headers['Content-Length'])
      request_data = self.rfile.read(content_length)

    method = getattr(requests, self.command.lower(), requests.get)
    resp = method(url, data=request_data, timeout=90)

    self.send_response(resp.status_code)
    self.send_header('Content-type', resp.headers['Content-Type'])
    self.end_headers()
    self.wfile.write(resp.content)


if __name__ == '__main__':
  app = server.HTTPServer(('localhost', 8080), Handler)
  print('Serving on http://localhost:8080/followers')
  app.serve_forever()

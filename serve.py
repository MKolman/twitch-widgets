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

  def do_GET(self):
    path_parts = self.path.strip('/').split('/')
    for n in range(len(path_parts), 0, -1):
      handler_name = '_'.join(path_parts[:n])
      if hasattr(self, handler_name):
        handler = getattr(self, handler_name)
        handler()
        break
    else:
      pass

  def followers(self):
    with open('followers.html', 'r') as template:
      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.end_headers()
      content = self._replace_template_variables(template.read())
      self.wfile.write(content.encode())

  def url(self):
    url = self.path[5:]
    print("Fetching", url)
    resp = requests.get(url)
    self.send_response(resp.status_code)
    self.send_header('Content-type', resp.headers['Content-Type'])
    self.end_headers()
    self.wfile.write(resp.content)


if __name__ == '__main__':
  app = server.HTTPServer(('localhost', 8080), Handler)
  print('Serving on http://localhost:8080/followers')
  app.serve_forever()

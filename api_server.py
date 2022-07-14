"""
backend api server
"""
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

HOST = '0.0.0.0'
PORT = os.environ.get('SIMPLE_API_PORT', 8082)


def get_ans(calc_type, params):
    param_x = params["x"]
    param_y = params["y"]

    if calc_type == '/plus':
        return param_x + param_y

    if calc_type == '/minus':
        return param_x - param_y

    raise Exception("invalid operation")


class APIHandler(BaseHTTPRequestHandler):
    """
    api handler
    """
    def do_GET(self):
        response = {}
        try:
            parsed_url = urlparse(self.path)
            calc_type = parsed_url.path

            params = {k: int(v[0]) for k, v in parse_qs(parsed_url.query).items()}
            ans = get_ans(calc_type, params)
            response = {
                'query': self.path,
                'response': ans
            }
            self.write_response(200, response)
        except:
            self.write_response(500, response)

    def write_response(self, status, response):
        body = json.dumps(response)
        self.send_response(status)
        self.send_header('Content-type', 'text/json; charset=utf-8')
        self.send_header('Content-length', len(body.encode()))
        self.end_headers()
        self.wfile.write(body.encode())


if __name__ == '__main__':
    httpd = HTTPServer((HOST, PORT), APIHandler)
    print(f"start port={PORT}")
    httpd.serve_forever()

from http.server import BaseHTTPRequestHandler
from io import BytesIO

# RFC 2616 describes the HTTP/1.1 protocol

class HTTPRequest(BaseHTTPRequestHandler):
    """
    Reference: https://stackoverflow.com/questions/4685217/parse-raw-http-headers
    """
    def __init__(self, request_text):
        self.rfile = BytesIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message

def parse_response(response):
    return

def parse_request(request):
    request = HTTPRequest(buf)

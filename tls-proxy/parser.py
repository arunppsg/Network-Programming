
# RFC 2616 describes the HTTP/1.1 protocol
# https://stackoverflow.com/questions/4685217/parse-raw-http-headers
HTTPRequestMethods = [
    'OPTIONS','GET', 'HEAD', 'POST',
    'PUT', 'DELETE', 'CONNECT', 'TRACE'
]

CRLF = '\r\n'
COLON = ':'
WHITESPACE = ' '
COMMA = ','
DOT = '.'
SLASH = '/'
HTTP_1_1 = 'HTTP/1.1'

def find_http_line(raw):
    pos = raw.find(CRLF)
    if pos == -1:
        return None, raw
    else:
        line = raw[:pos]
        rest = raw[pos+len(CRLF):]
        return line, rest

def get_request_uri(raw):
    return uri

def parse_response(response):
    return

def parse_request(request):
    request = request.decode('iso-8859-1')
    more = True if len(raw) > 0 else False
    while more:
        
    header, body = find_http_line(request)
    if header is None:
        return
    uri = get_request_uri(body) 
    request = request.split('\r\n')
    if request[0] == 'CONNECT':
        
    return

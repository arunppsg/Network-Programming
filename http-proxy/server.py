import socket


def handle_request(sock, cliaddr):
    request_str = sock.recv(1024).decode('latin-1')
    request = request_str.split('\n')
    url_line = request[0]
    url = url_line.split(' ')[1]

    # Extract URL from request
    # Example 1: url before: http://www.google.com, after: www.google.com
    # Example 2: url before: www.google.com, after: www.google.com
    colon_slash = url.find("://")
    if (colon_slash == -1):
        pass 
    else:
        url = url[(colon_slash+3):] 

    # Gets the server position
    # Example: www.example.com/index.html, webserver_pos = 15
    webserver_pos = url.find("/")
    if webserver_pos == -1:
        webserver_pos = len(url)

    webserver = ""
    port_pos = url.find(":")
    if (port_pos == -1 or webserver_pos < port_pos):
        # default port 
        port = 80 
        webserver = url[:webserver_pos] 

    else:
        port = int(url[(port_pos+1):][:webserver_pos - port_pos - 1])
        webserver = url[:port_pos]

    upstream_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    upstream_sock.connect((webserver, port))
    upstream_sock.sendall(request_str.encode('latin-1'))

    while True:
        response = upstream_sock.recv(1024)
    
        if (len(response) > 0):
            sock.send(response)
        else:
            break
        return

def initialize_socket(server_address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(server_address)
    request_queue_size = 50
    sock.listen(request_queue_size)
    return sock

def start_server(server_address):
    sock = initialize_socket(server_address)
    while True:
        clisock, cliaddr = sock.accept()
        handle_request(clisock, cliaddr)

if __name__ == "__main__":
    start_server(("127.0.0.1", 8998))

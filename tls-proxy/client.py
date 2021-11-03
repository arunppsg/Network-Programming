import socket
import ssl

if __name__ == "__main__":
    hostname = "www.google.com"
    port = 443
    sock = socket.create_connection((hostname, port))
    context = ssl.create_default_context()
    ssock = context.wrap_socket(sock, server_hostname=hostname)

    ssock.write(buf)
    buf = ssock.read()
    parser.parse(buf)

import socket
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# The private key of server and its certificate. The client
# encrypts connection with the key in the certificate
context.load_cert_chain('/path/to/certchain.pem', '/path/to/private.key')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(('127.0.0.1', 8443))
    sock.listen(5)
    with context.wrap_socket(sock, server_side=True) as ssock:
        conn, addr = ssock.accept()

if __name__ == "__main__":
    start_server(("127.0.0.1", 8998))


def get_server_certificate((hostname, port)):
    try:
        ssl.get_server_certificate((hostname, port))
    except ssl.SSLError:
        pass

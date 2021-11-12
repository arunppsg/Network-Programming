"""
A HTTP Proxy

Based on https://github.com/abhinavsingh/proxy.py/commit/cffbc48c062423420f6c1e209ad3675a9354e698
"""

import os
import socket
import select
import datetime
import multiprocessing
from io import BytesIO
from http.server import BaseHTTPRequestHandler
import logging

logging.basicConfig(filename='proxy.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Connection(object):
    def __init__(self, server_client):
        self.closed = False
        self.buffer = b''
        self.server_client = server_client

    def recv(self, buf_size=8192):
        data = self.conn.recv(buf_size)
        return data

    def send(self, data):
        return self.conn.send(data)

    def close(self):
        self.conn.close()
        self.closed = True

    def buffer_size(self):
        return len(self.buffer)

    def has_buffer(self):
        return self.buffer_size() > 0

    def queue(self, data):
        self.buffer += data

    def flush(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]


class Server(Connection):
    def __init__(self, host, port):
        super().__init__('server')
        self.addr = (host, int(port))

    def connect(self): 
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.conn.connect(self.addr)

class Client(Connection):
    def __init__(self, conn, addr):
        super().__init__('client')
        self.conn = conn
        self.addr = addr


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = BytesIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message

    def is_parsed(self):
        if self.error_code is None: 
            return True
        else:
            return False

    def get_host_port(self): 
        host_port = self.headers['Host'].split(':') 
        if len(host_port) == 1:
            return host_port[0], 80
        else:
            return host_port[0], host_port[1]

class Proxy(multiprocessing.Process):
    def __init__(self, client):
        super(Proxy, self).__init__()
        self.start_time = self._now()
        self.last_activity = self.start_time

        self.client = client
        self.server = None

    def _now(self):
        return datetime.datetime.now()

    def _inactive_for(self):
        return (self._now() - self.last_activity).seconds

    def _is_inactive(self):
        return self._inactive_for() > 30

    def _process(self):
        #print ("Processing connection \n")
        while True:
            rlist, wlist, xlist = self._get_waitable_list()
            r, w, x = select.select(rlist, wlist, xlist, 1)
    
            self._process_wlist(w)
            if self._process_rlist(r):
                break

            if self.client.buffer_size() == 0:
                if self._is_inactive():
                    break

    def _process_request(self, data):
        # Once there is connection to server, parsing of htttp
        # request packets is not needed. We just pip data from client
        # to server
        
        if self.server and not self.server.closed:
            self.server.queue(data)
            return

        request = HTTPRequestHandler(data)
        # print ("Received request ", data)
        # When a request comes in, we open a connection to the upstream server
        if request.is_parsed():
            host, port = request.get_host_port() 
            # print ("Server host, port ", host, port)

        self.server = Server(host, port)
        self.server.connect()
        self.server.queue(data)

    def _process_response(self, data):
        self.client.queue(data)

    def _get_waitable_list(self):
        #  User Application --client.conn--> Proxy --server.conn--> Web Server
        #  If the client has data which is to be sent (written) to the
        #  proxy server, it gets added to the wlist.
        rlist, wlist, xlist = [self.client.conn], [], []

        if self.client.has_buffer():
            wlist.append(self.client.conn)

        if self.server and not self.server.closed:
            rlist.append(self.server.conn)
            if self.server.has_buffer():
                wlist.append(self.server.conn)

        return rlist, wlist, xlist

    def _process_wlist(self, w):
        if self.client.conn in w:
            self.client.flush()

        if self.server and not self.server.closed:
            if self.server.conn in w:
                self.server.flush()

    def _process_rlist(self, r):
        """Returns True if there is no data from client else
            False
        """
        # print ("In process rlist ")
        if self.client.conn in r:
            data = self.client.recv()
            self._last_activity = self._now()
            if not data:
                return True
            # print ("Received ", data)
            self._process_request(data) 

        if self.server and not self.server.closed:
            if self.server.conn in r:
                data = self.server.recv()
                self._last_activity = self._now()
                if not data: 
                    self.server.close()
                else: 
                    self._process_response(data)

        return False

    def run(self):
        try:
            self._process()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            logger.exception('Exception while handling connection %r with reason %r' % (self.client.conn, e))
        finally:
            logger.debug('closing client connection')

class Http(object):
    
    def __init__(self, hostname='127.0.0.1', port=8899, backlog=50):
        self.hostname = hostname
        self.port = port
        self.backlog = backlog

    def run(self):

       print('Starting proxy server at host %s port %s' % (self.hostname, self.port))
       self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
       self.socket.bind((self.hostname, self.port))
       self.socket.listen(self.backlog)

       while True:
           conn, addr = self.socket.accept()
           logger.info("Accepted a connection at %r at address %r" % (conn, addr))
           client = Client(conn, addr)
           proc = Proxy(client) 
           proc.start()
 
       self.socket.close()
                
if __name__ == "__main__":
    http = Http()
    http.run()


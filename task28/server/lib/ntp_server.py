import time
import logging
import SocketServer
import struct
from daemonize import Daemonize
 
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8080
BUF_SIZE = 8192
 
pid = '/tmp/TimeServer.pid'
 
logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)
 
fh = logging.FileHandler('TimeServer.log')
fh.setLevel(logging.DEBUG)
 
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
 
logger.addHandler(fh)
 
keep_fds = [fh.stream.fileno()]
 
class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
 
    def handle(self):
        while True:
            try:
                data = self.request.recv(BUF_SIZE)
                if not data:
                    break
                logger.info("Received: IP:%s message: %s" % (self.client_address[0], data))
                i1, i2, message = struct.unpack('!2b8s', data)
                if i1 == 3 and i2 == 7 and message == 'get_time':
                    cur_time = int(time.time())
                    response = struct.pack('>2bi', i1, i2, cur_time)
                    self.request.sendall(response)
                    logger.info("Send: IP:%s message: %s" % (self.client_address[0], cur_time))
                else:
                    logger.error("Message Error!")
            except(Exception):
                logger.error("遇到错误：" + str(e))
                break
 
    def finish(self):
        self.request.close()
 
 
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass
''' 
def main():
    server = ThreadedTCPServer((SERVER_HOST, SERVER_PORT), ThreadedTCPRequestHandler)
    print "Server Loop Running..."
    server.serve_forever()
 
#main()
 
daemon = Daemonize(app="TimeServer", pid=pid, action=main, keep_fds=keep_fds)
daemon.start()
'''
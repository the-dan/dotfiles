#!/usr/bin/python
# This is a simple port-forward / proxy, written using only the default python
# library. If you want to make a suggestion or fix something you can contact-me
# at voorloop_at_gmail.com
# Distributed over IDC(I Don't Care) license
# http://voorloopnul.com/blog/a-python-proxy-in-less-than-100-lines-of-code/
import socket
import select
import time
import sys
import logging

# Changing the buffer_size and delay, you can improve the speed and bandwidth.
# But when buffer get to high or delay go too down, you can broke things
buffer_size = 4096
delay = 0.0001


class Forward:
    def __init__(self):
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        try:
            self.forward.connect((host, port))
            return self.forward
        except Exception, e:
            print e
            return False

class TheServer:
    input_list = []
    channel = {}
    fwds = []
    rh = ''
    rp = 80

    def __init__(self, host, port, rh, rp):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.rh = rh
        self.rp = rp
        self.server.listen(200)

    def main_loop(self):
        self.input_list.append(self.server)
        while 1:
            time.sleep(delay)
            ss = select.select
            inputready, outputready, exceptready = ss(self.input_list, [], [])
            for self.s in inputready:
                if self.s == self.server:
                    self.on_accept()
                    break

                is_fwd = False
                if self.s in self.fwds:
                    is_fwd = True
                
                if is_fwd:
                    logging.debug("Reading from forward")
                else:
                    logging.debug("Reading from requester")
                        
                try:
                    self.data = self.s.recv(buffer_size)
                    
                    if len(self.data) == 0:
                        logging.debug("closing")
                        self.on_close(is_fwd)
                    else:
                        logging.debug("recving")
                        self.on_recv(is_fwd)
                except socket.error:
                    logging.debug("closing")
                    self.on_close(is_fwd)

    def on_accept(self):
        forward = Forward().start(rh, rp)
        clientsock, clientaddr = self.server.accept()
        if forward:
            logging.info(repr(clientaddr) + " has connected")
            self.fwds.append(forward)
            self.input_list.append(clientsock)
            self.input_list.append(forward)
            self.channel[clientsock] = forward
            self.channel[forward] = clientsock
        else:
            logging.warn("Can't establish connection with remote server")  
            logging.warn("Closing connection with client side %s", repr(clientaddr))
            clientsock.close()

    def on_close(self, is_fwd):
        peername = "<unknown>"
        try:
            self.s.getpeername()
        except socket.error:
            None
        
        if is_fwd:
            logging.debug("Closing forward %s", repr(peername))
            self.fwds.remove(self.s)
        else:
            logging.debug("Closing requester %s", repr(peername))
        
        self.input_list.remove(self.s)
        self.s.close();
        del self.channel[self.s]
        

    def on_recv(self, is_fwd):
        data = self.data
        # here we can parse and/or modify the data before send forward
        char = "->"
        if is_fwd:
            char = "<-"
        print "%s[%s]" % (char, data)
        self.channel[self.s].send(data)

if __name__ == '__main__':
        if len(sys.argv) < 2:
            print "Usage: %s [<bind_addr>]:<bind_port>:<remote_addr>:<remote_port>" % (sys.argv[0], )
            exit(1)

        conn_str = sys.argv[1]
        params = conn_str.split(":")
        try:
            rp = int(params[-1])
            rh = params[-2]
            bp = int(params[-3])
        except IndexError:
            print "wrong number of arguments"
            exit(1)
        bh = ''
        try:
            bh = params[-4]
        except IndexError:
            None

        logging.basicConfig(level="DEBUG", format="%(asctime)s %(message)s")
            
        server = TheServer(bh, bp, rh, rp)
        try:
            server.main_loop()
        except KeyboardInterrupt:
            print "Ctrl C - Stopping server"
            sys.exit(1)
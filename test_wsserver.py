#!/usr/bin/python

# status
#   0   Nothing to do
#   1   HandShake OK to network
#   2   HandShake NOK to network
#   3   Data (frame encoded) to network
#   4   Pong (After receiving a Ping) to network
#   5   Close (After receiving close) to network
#   8   Data (frame decoded) to application

import SocketServer
import wsserver

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    
    """
    def application(self,instance,buffer):
        instance.sendData("hello World",0x1)
        if instance.status() == 3:
            print "Data frame to network"
            response = instance.result()
            self.request.sendall(response)
            print "send: \n%s" % response

    def handle(self):
        # self.request is the TCP socket connected to the client
        print "connected"
        instance = wsserver.wsserver()
        data = self.request.recv(1024)
        while len(data):
            print "received: \n%s" % data
            #state = instance.state()
            instance.dataRecv(data)
            status = instance.status()
            # send to client
            if status in [1,2,3,4,5]:
                if status == 1:
                    print "Handshake OK"
                elif status == 2:
                    print "Handshake NOK"
                elif status == 3:
                    print "Data frame to network"
                elif status == 4:
                    print "PONG to network"
                elif status == 5:
                    print "CLOSE to network"
                else:
                    pass
                response = instance.result()
                self.request.sendall(response)
                print "send: \n%s" % response
            # send to application
            elif status == 8:
                print "Data to application"
                response = instance.result()
                print response
                self.application(instance,response)
            data = self.request.recv(1024)
        print "disconnected"
        self.request.close()

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9998
    server =  ThreadedTCPServer((HOST, PORT), MyTCPHandler)
    print "started ..."
    server.serve_forever()
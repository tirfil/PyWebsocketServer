#!/usr/bin/python

#    Copyright 2014 Philippe THIRION
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
        #instance.sendData("hello World",0x1)
        instance.sendClose("toto")
        print "state %d (2)" % instance.state()
        if instance.status() == 3:
            print "Data frame to network (2)"
            response = instance.result()
            self.request.sendall(response)
            print "send: \n%s (2)" % response

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
            print "state %d" % instance.state()
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
            else:
                #0
                print "status is 0"
            data = self.request.recv(1024)
        print "disconnected"
        self.request.close()

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9998
    server =  ThreadedTCPServer((HOST, PORT), MyTCPHandler)
    print "started ..."
    server.serve_forever()
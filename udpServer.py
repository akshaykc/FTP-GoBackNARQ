'''
Created on Apr 13, 2016

@author: achaluv
'''
import socket
import threading


class udpServer(threading.Thread):
    def __init__(self, name, hostName, udpServerPort, fileName, packetLossProb):
        threading.Thread.__init__(self)
        self.name = name
        self.hostName = hostName
        self.udpServerPort = udpServerPort
        self.fileName = fileName
        self.packetLossProb = packetLossProb
    
    
    
    def run(self):
        print "thread start server\n"
        
        sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.hostName, self.udpServerPort))
        
        while True:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            print "received message:", data, addr
            
        sock.close()
        print "Server closed"
'''
Created on Apr 13, 2016

@author: achaluv
'''
import socket
import threading
import segment

headerLen = 8

class udpClient(threading.Thread):
    def __init__(self, name, hostName, udpServerPort, fileName, WindowSize, MSS):
        threading.Thread.__init__(self)
        self.name = name
        self.hostName = hostName
        self.udpServerPort = udpServerPort
        self.fileName = fileName
        self.WindowSize = WindowSize
        self.bufSize = WindowSize
        self.MSS = MSS
        self.segSize = MSS + headerLen
        self.bufHead = 0
        self.bufTail = 0
        self.mutex = threading.Semaphore(1)
        self.empty = threading.Semaphore(WindowSize)
        self.item = threading.Semaphore(0)
        self.buffer = [None for i in range(self.bufSize)]
        self.timer = [None for i in range(self.bufSize)]
        
        self.sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    
    def sendToServer(self, segment):
        self.empty.acquire()
        self.mutex.acquire()
        
        self.buffer[self.bufTail] = segment
        self.sock.sendto("segment.getData()", (self.hostName, self.udpServerPort))
        
        self.timer[self.bufTail] = threading.Timer(0.2, self.retransmitTimer, [self.bufTail])
        self.timer[self.bufTail].start()
        
        self.bufTail = (self.bufTail + 1) % self.bufSize
        
        self.mutex.release()
        self.item.release()
        
        
    def rdt_send(self):
        slidingWindowProtocol = self.slidingWindow(self.sock)
        slidingWindowProtocol.start()
        seqNo = 0
        count = 0
        data = bytearray([0 for _ in range(self.MSS)])
        with open(self.fileName, "rb") as inputFile:
            byte = inputFile.read(1)
            while byte != "":
                data[count] = byte
                count = count + 1
                if count == self.MSS:
                    self.sendToServer(segment(seqNo, count, data))
                    seqNo = seqNo + count
                    count = 0
                    data = [0 for _ in range(self.MSS)]
                byte = inputFile.read(1)
        
    def run(self):
        print "thread start client"
        self.rdt_send()
        
        #print "UDP target IP:", self.hostName
        #print "UDP target port:", self.udpServerPort
        #print "message:", message
        print "Client closed"
        
    
    def retransmitTimer(self, index):
        print "Timeout for sequence number ", buffer[index].getSeqNo()
        self.sock.sendto(buffer[index].getData(),(self.hostName, self.udpServerPort))
        self.timer[self.bufTail].start()
        
        
        
            
    class slidingWindow(threading.Thread):
        def __init__(self, sock):
            threading.Thread.__init__(self)
            self.runState = True
            self.sock = sock
            
        def run(self):
            while self.runState:
                data, addr = self.sock.recvfrom(1024)
                print "Received message :", data
                recvdSegment = segment.segmentResponse(data, len(data))
                if recvdSegment.type() == 1:
                    if recvdSegment.getSeqNo() == buffer[self.bufHead].getSeqNo() + \
                                            buffer[self.bufHead].getDataSize():
                        self.processRcvdSegment(recvdSegment)
                    #elif recvdSegment.getSeqNo() == buffer[self.bufHead].getSeqNo():
        
        def processRcvdSegment(self, segment):
            self.item.acquire()
            self.mutex.acquire()
            
            self.timer[self.bufHead].cancel()
            self.bufHead = (self.bufHead + 1) % self.bufSize
            
            self.mutex.release()
            self.empty.release()
                        
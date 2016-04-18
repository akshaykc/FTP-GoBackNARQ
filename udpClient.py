'''
Created on Apr 13, 2016

@author: achaluv
'''
import socket
import threading
import segment

headerLen = 8

bufHead = 0
bufTail = 0
bufferWindow = []
bufSize = 0
timer = []
class udpClient(threading.Thread):
    def __init__(self, name, hostName, udpServerPort, fileName, WindowSize, MSS):
        threading.Thread.__init__(self)
        global bufSize
        global bufferWindow
        global timer
        self.name = name
        self.hostName = hostName
        self.udpServerPort = udpServerPort
        self.fileName = fileName
        self.WindowSize = WindowSize
        self.MSS = MSS
        self.segSize = MSS + headerLen
        self.mutex = threading.Semaphore(1)
        self.empty = threading.Semaphore(WindowSize)
        self.item = threading.Semaphore(0)
        bufSize = WindowSize
        self.retrasmiTO = 0.5
        bufferWindow = [None for i in range(0,bufSize)]
        timer = [None for i in range(bufSize)]
        
        
        
        self.sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    
    def sendToServer(self, segment):
        global bufferWindow
        global bufTail
        global bufHead
        global bufSize
        global timer
        
        self.empty.acquire()
        self.mutex.acquire()
        
        bufferWindow[bufTail] = segment
        dataToSend = bytearray(segment.getData())
        
        self.sock.sendto(dataToSend, (self.hostName, self.udpServerPort))
        
        timer[bufTail] = threading.Timer(self.retrasmiTO, self.retransmitTimer, [bufTail])
        timer[bufTail].start()
        
        bufTail = (bufTail + 1) % bufSize
        
        self.mutex.release()
        self.item.release()
        
        
    def rdt_send(self):
        slidingWindowProtocol = self.slidingWindow(self.sock)
        slidingWindowProtocol.start()
        seqNo = 0
        count = 0
        data = []
        with open(self.fileName, "rb") as inputFile:
            byte = inputFile.read(1)
            while True:
                if  byte != "":
                    data.append(byte)
                    count = count + 1
                if count == self.MSS or byte == "":
                    segmentToSend = segment.segment(seqNo, count, data)
                    self.sendToServer(segmentToSend)
                    seqNo = seqNo + count
                    count = 0
                    data = [0 for _ in range(0,len(data))]
                    if  byte == "":
                        break
                byte = inputFile.read(1)
        
    def run(self):
        print "thread start client"
        self.rdt_send()
        
        #print "UDP target IP:", self.hostName
        #print "UDP target port:", self.udpServerPort
        #print "message:", message
        print "Client closed"
        
    
    def retransmitTimer(self, index):
        global bufferWindow
        global bufTail
        global timer
        self.retrasmiTO = 0.5
        print "Timeout for sequence number ", bufferWindow[index].getSeqNo()
        data = bufferWindow[index].getData()
        dataToSend = bytearray(data)
        self.sock.sendto(dataToSend,(self.hostName, self.udpServerPort))
        timer[index].start()
            
    class slidingWindow(threading.Thread):
        def __init__(self, sock):
            threading.Thread.__init__(self)
            self.runState = True
            self.sock = sock
            
        def run(self):
            while self.runState:
                global bufHead
                data, addr = self.sock.recvfrom(1024)
                data = bytearray(data)
                print "Received message :", data
                recvdSegment = segment.segmentResponse(data, len(data))
                typeSim = recvdSegment.getType()
                if recvdSegment.getType() == 1:
                    recvdSegmentSeqNo = recvdSegment.getSeqNo()
                    print type(buffer[bufHead])
                    bufferSegmentSeqNo = buffer[bufHead].getSeqNo()
                    bufferSegmentDataSize = buffer[bufHead].getDataSize()
                    if recvdSegment.getSeqNo() == buffer[bufHead].getSeqNo() + buffer[bufHead].getDataSize():
                        self.processRcvdSegment(recvdSegment)
                    #elif recvdSegment.getSeqNo() == buffer[self.bufHead].getSeqNo():
        
        def processRcvdSegment(self, segment):
            global bufHead
            global bufSize
            global timer
            self.item.acquire()
            self.mutex.acquire()
            
            timer[bufHead].cancel()
            bufHead = (bufHead + 1) % bufSize
            
            self.mutex.release()
            self.empty.release()
                        
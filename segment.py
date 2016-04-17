import struct

headerLen = 8

class segment():
    def __init__(self, seqNo, size, data):
        self.data[headerLen:] = bytearray(data)
        self.seqNo = seqNo
        self.type = 0
        self.checkSum = self.check(self.data)
        
        self.size = size
        #Assign sequence number
        self.data[0:4] = bytearray(struct.pack("!I", self.seqNo))
        #Assign checksum
        self.data[4] = 0#checksum
        self.data[5] = 0#checksum
        #Assign indicating data packet
        self.data[6] = 0x55
        self.data[7] = 0x55

    def getData(self):
        return self.data
    
    def getSize(self):
        return len(self.data)
    
    def check(self):
        return 0
    
    def type(self):
        return self.type
        
    def getSeqNo(self):
        return self.seqNo
    
    def getDataSize(self):
        return len(self.data) - headerLen
        
class segmentResponse():
    def __init__(self, data, size):
        self.data[:] = bytearray(data)
        self.seqNo = struct.unpack('>I', self.data[0:4])
        if self.data[6] == 0x55 &  self.data[7] == 0x55:
            self.type = 0
        elif self.data[6] == 0xAA &  self.data[7] == 0xAA:
            self.type = 1
            
    def getData(self):
        return self.data
    
    def getSize(self):
        return len(self.data)
    
    def check(self):
        return 0
    
    def type(self):
        return self.type
        
    def getSeqNo(self):
        return self.seqNo
    
    def getDataSize(self):
        return len(self.data) - headerLen
    
class segmentAck():
    def __init__(self, nextSeqNo, size):
        self.data = bytearray([0 for _ in range(size)])
        self.seqNo = nextSeqNo
        self.data[0:4] = bytearray(struct.pack("!I", self.seqNo))
        #Assign indicating Ack packet
        self.data[6] = 0xAA
        self.data[7] = 0xAA
        self.checkSum = self.check()
        
    def getData(self):
        return self.data
    
    def getSize(self):
        return len(self.data)
    
    def check(self):
        return 0
    
    def type(self):
        return self.type
        
    def getSeqNo(self):
        return self.seqNo
    
    def getDataSize(self):
        return len(self.data) - headerLen
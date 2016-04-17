'''
Created on Apr 16, 2016

@author: achaluv
'''

import udpClient
import udpServer

def main():
    print "strng"

if __name__ == '__main__':
    # Create new threads
    #name, hostName, udpServerPort, fileName, packetLossProb
    udpServerThread = udpServer.udpServer("udpServer", 
                            'localhost', 7735, "serverOutput.txt", 0)
    # name, hostName, udpServerPort, fileName, WindowSize, MSS
    udpClientThread = udpClient.udpClient("udpClient", 
                            'localhost', 7735, "clientInput.txt", 10, 100)
    
    udpServerThread.start()
    udpClientThread.start()
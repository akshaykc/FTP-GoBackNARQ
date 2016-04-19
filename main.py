'''
Created on Apr 16, 2016

@author: achaluv
'''

import udpClient
import udpServer


if __name__ == '__main__':
    # Create new threads
    #port# file-name p
    udpServer = udpServer.udpServer(7735, "serverOutput.txt", 0.05)
    #server-host-name server-port file-name N MSS
    udpClient = udpClient.udpClient('localhost', 7735, 
                                          "clientInput.txt", 10, 500)
    
    udpServer.start()
    udpClient.start()
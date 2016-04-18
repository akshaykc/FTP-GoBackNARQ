'''
Created on Apr 16, 2016

@author: achaluv
'''

import udpClient
import udpServer


if __name__ == '__main__':
    # Create new threads
    udpServerThread = udpServer.udpServer("udpServer", 
                            'localhost', 7735, "serverOutput.txt", 0)
    udpClientThread = udpClient.udpClient("udpClient", 
                            'localhost', 7735, "clientInput.txt", 10, 100)
    
    udpServerThread.start()
    udpClientThread.start()
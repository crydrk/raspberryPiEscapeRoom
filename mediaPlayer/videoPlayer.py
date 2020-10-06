import pygame
import socket
import os

from subprocess import Popen


mediaDict = {}

# UPD setup
UDP_PORT = 2522
UDP_IP = ""
INCOMING_IP = ""

#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.bind((UDP_IP, UDP_PORT))

globalFilepath = "/home/pi/mediaPlayer"
try:
    globalFilepath = os.path.dirname(os.path.abspath(__file__))
    print globalFilepath
except:
    pass

def RunDevice():
    
    moviePath = globalFilepath + "/mediaFiles_video/magicShowStart.mp4"
    
    omxp = Popen(['omxplayer', moviePath])

    """
    while True:
        data, addr = sock.recvfrom(1024)
        ReceiveData(data, addr)
        """

def ReceiveData(data, addr):
    print data
    print addr
    
    INCOMING_IP = addr[0]
    
    if data == "verify":
        print "trying to verify"
        sock.sendto("good", (INCOMING_IP, UDP_PORT))
        
    if data in audioDict.keys():
        # Play the audio if it matches the incoming message
        pygame.mixer.Sound.play(audioDict[data])
        
        while pygame.mixer.Channel(0).get_busy() == True:
            continue
            
        # Workaround to remove any data that came in during audio
        sock.setblocking(0)
        while 1:
            try:
                throwaway = sock.recvfrom(1024)
            except:
                break
        sock.setblocking(1)
    
    
    
RunDevice()
    

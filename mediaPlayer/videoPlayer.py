import pygame
import socket
import os
import select

import subprocess
from subprocess import Popen

from time import sleep

mediaDict = {}

# UPD setup
UDP_PORT = 1885
UDP_IP = ""
INCOMING_IP = ""

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

globalFilepath = "/home/pi/mediaPlayer"
try:
    globalFilepath = os.path.dirname(os.path.abspath(__file__))
    print globalFilepath
except:
    pass
    
videoDict = {}

def RunDevice():
    
    (w, h) = (1200, 900)
    screen = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
    pygame.display.flip()
    
    pygame.mouse.set_visible(False)
    
    videoDict["test"] = globalFilepath + "/mediaFiles_video/magicShowStart.mp4"
    
    while True:
        r, _, _ = select.select([sock], [], [])
        if r:
            data, addr = sock.recvfrom(1024)
            ReceiveData(data, addr)
                    
        sleep(1)

def ReceiveData(data, addr):
    print data
    print addr
    
    INCOMING_IP = addr[0]
    
    if data == "verify":
        print "trying to verify"
        sock.sendto("good", (INCOMING_IP, UDP_PORT))
        
    if data == "quit":
        pygame.quit()
        exit()
        
    if data == "kill":
        os.system('killall omxplayer.bin')
        
    if data in videoDict.keys():
        os.system('killall omxplayer.bin')
        
        # Play the video if it matches the incoming message
        dur = subprocess.check_output("avconv -i " + videoDict[data] + " 2>&1 | grep Duration | cut -d ' ' -f 4 | sed s/,//", shell=True)
    
        # dur's time format will be: 00:02:21.18
        minutes = dur.split(':')[1]
        seconds = dur.split('.')[0].split(':')[2]
        
        seconds = int(minutes) * 60 + int(seconds) + 1 # Some extra leeway for loading - this number doesn't need to be spot on
        
        omxp = Popen(['omxplayer', videoDict[data]])
        
        return
    
    
    
RunDevice()
    

import pygame
import socket
import os

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
    
    videoDict["test"] = globalFilepath + "/mediaFiles_video/magicShowStart.mp4"
    
    while True:
        WaitForDataOrQuit()
                    
        sleep(1)
        
def WaitForDataOrQuit():
    
    data, addr = sock.recvfrom(1024)
    ReceiveData(data, addr)
    
    # Check for quit
    for event in pygame.event.get():
        if event.type == QUIT:
            return
        elif event.type == KEYDOWN:
            if event.key == "escape":
                pygame.quit()
                return

def ReceiveData(data, addr):
    print data
    print addr
    
    INCOMING_IP = addr[0]
    
    if data == "verify":
        print "trying to verify"
        sock.sendto("good", (INCOMING_IP, UDP_PORT))
        
    if data in videoDict.keys():
        # Play the video if it matches the incoming message
        dur = subprocess.check_output("avconv -i " + videoDict[data] + " 2>&1 | grep Duration | cut -d ' ' -f 4 | sed s/,//", shell=True)
    
        # dur's time format will be: 00:02:21.18
        minutes = dur.split(':')[1]
        seconds = dur.split('.')[0].split(':')[2]
        
        seconds = int(minutes) * 60 + int(seconds) + 1 # Some extra leeway for loading - this number doesn't need to be spot on
        
        omxp = Popen(['omxplayer', videoDict[data]])
        
        print "starting sleep"
        sleep(seconds)
            
        # Workaround to remove any data that came in during video
        sock.setblocking(0)
        while 1:
            try:
                throwaway = sock.recvfrom(1024)
            except:
                break
        sock.setblocking(1)
    
    
    
RunDevice()
    

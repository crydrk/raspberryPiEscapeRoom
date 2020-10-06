import pygame
import socket
import os

import subprocess
from subprocess import Popen

from time import sleep


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
    
    dur = subprocess.check_output("avconv -i " + globalFilepath + "/mediaFiles_video/magicShowStart.mp4" + " 2>&1 | grep Duration | cut -d ' ' -f 4 | sed s/,//", shell=True)
    
    # dur's time format will be: 00:02:21.18
    
    minutes = dur.split(':')[1]
    seconds = dur.split('.')[0].split(':')[2]
    
    print "minutes: " + minutes
    print "seconds: " + seconds
    
    milliseconds = int(minutes) * 60 * 1000 + int(seconds) * 1000
    milliseconds += 1000 # Some extra leeway for loading - this number doesn't need to be spot on
    
    print milliseconds / 1000
    print milliseconds
    
    moviePath = globalFilepath + "/mediaFiles_video/magicShowStart.mp4"
    omxp = Popen(['omxplayer', moviePath])
    
    print "starting sleep"
    sleep(milliseconds / 1000)
    print "ending sleep"
    
    moviePath = globalFilepath + "/mediaFiles_video/magicShowStart.mp4"
    omxp = Popen(['omxplayer', moviePath])
    
    #VIDEO_PATH = globalFilepath + "/mediaFiles_video/magicShowStart.mp4"
    #player = OMXPlayer(VIDEO_PATH)
    
    sleep(30)
    
    player.quit()
    
    #moviePath = globalFilepath + "/mediaFiles_video/magicShowStart.mp4"
    
    #omxp = Popen(['omxplayer', moviePath])

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
    

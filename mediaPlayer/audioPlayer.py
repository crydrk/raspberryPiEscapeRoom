import pygame
import socket
import os


audioDict = {}

# UPD setup
UDP_PORT = 2522
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

def RunDevice():
    
    # Initialize the mixer
    pygame.mixer.init()

    # Load the audio files
    redAudio = pygame.mixer.Sound(globalFilepath + "/mediaFiles_audio/001_red.wav")
    yellowAudio = pygame.mixer.Sound(globalFilepath + "/mediaFiles_audio/002_yellow.wav")
    blueAudio = pygame.mixer.Sound(globalFilepath + "/mediaFiles_audio/003_blue.wav")
    greenAudio = pygame.mixer.Sound(globalFilepath + "/mediaFiles_audio/004_green.wav")
    
    audioDict["Gryffindor"] = redAudio
    audioDict["Hufflepuff"] = yellowAudio
    audioDict["Ravenclaw"] = blueAudio
    audioDict["Slytherin"] = greenAudio

    # Short delay while running processor to allow for loading
    pygame.time.delay(3000)

    
    while True:
        data, addr = sock.recvfrom(1024)
        ReceiveData(data, addr)

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
    

# Test plays
pygame.mixer.Sound.play(redAudio)

while pygame.mixer.Channel(0).get_busy() == True:
    continue
    
pygame.mixer.Sound.play(yellowAudio)

while pygame.mixer.Channel(0).get_busy() == True:
    continue
    
pygame.mixer.Sound.play(blueAudio)

while pygame.mixer.Channel(0).get_busy() == True:
    continue

pygame.mixer.Sound.play(greenAudio)

while pygame.mixer.Channel(0).get_busy() == True:
    continue

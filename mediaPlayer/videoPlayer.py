import pygame
import socket
import os


mediaDict = {}

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
    
    # Initialize the mixer, and immediately quit
    # This is a workaround suggested by bluegalaxy.info
    pygame.init()
    pygame.mixer.quit()
    clock = pygame.time.Clock()
    movie = pygame.movie.Movie(globalFilepath + "/mediaFiles_video/test.mpg")
    screen = pygame.display.set_mode(movie.get_size())
    movie_screen = pygame.Surface(movie.get_size()).convert()
    
    movie.set_display(movie_screen)
    movie.play()
    
    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                movie.stop()
                playing = False
                
    screen.blit(movie_screen, (0,0))
    pygame.display.update()
    clock.tick(FPS)
    
    pygame.quit()

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
    

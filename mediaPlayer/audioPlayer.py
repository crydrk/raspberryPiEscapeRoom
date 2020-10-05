import pygame

# Initialize the mixer
pygame.mixer.init()

# Load the audio files
redAudio = pygame.mixer.Sound("mediaFiles_audio/001_red.wav")
yellowAudio = pygame.mixer.Sound("mediaFiles_audio/002_yellow.wav")
blueAudio = pygame.mixer.Sound("mediaFiles_audio/003_blue.wav")
greenAudio = pygame.mixer.Sound("mediaFiles_audio/004_green.wav")

# Short delay while running processor to allow for loading
pygame.time.delay(3000)



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

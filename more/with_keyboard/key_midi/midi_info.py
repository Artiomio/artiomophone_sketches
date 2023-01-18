import pygame.midi
import time

pygame.midi.init()

for i in range(10):
    try:
        r = pygame.midi.get_device_info(i)
        print(r[1].decode(), "-", i)
    except:
        pass    

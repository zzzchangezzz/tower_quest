import pygame
import os
import sys


def terminate():
    pygame.quit()
    sys.exit()


def load_image(way, name, colorkey=None):
    fullname = os.path.join(way, name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

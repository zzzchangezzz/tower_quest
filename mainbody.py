import pygame, os, sys
import buttons
pygame.init()


class MenuWindow:
    def __init__(self):
        self.size = self.width, self.height = 640, 640
        self.butweight, self.butheight = 300, 80
        self.offset = 170
        self.space = 100
        self.clr = pygame.Color(0, 97, 100)
        self.run = True

    def mainmenu(self):
        pass
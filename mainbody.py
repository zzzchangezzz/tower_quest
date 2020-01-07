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


class Prologue:
    def __init__(self):
        self.size = self.width, self.height = 640, 640
        self.curr_cadr = -1
        self.all_cadr = 4
        self.naming = 'P0.png'
        self.running = True

    def terminate(self):
        pygame.quit()
        sys.exit()

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('prolog', name)
        image = pygame.image.load(fullname)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    def tellstory(self):
        screen = pygame.display.set_mode(self.size)
        while self.running:
            fon = pygame.transform.scale(self.load_image(self.naming), (self.width, self.height))
            screen.blit(fon, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.terminate()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.curr_cadr += 1
                    if self.curr_cadr > self.all_cadr:
                        running = False
                        return
                    else:
                        self.naming = 'P' + str(self.curr_cadr) + '.png'
                        fon = pygame.transform.scale(self.load_image(self.naming), (self.width, self.height))
                        screen.blit(fon, (0, 0))
            pygame.display.flip()

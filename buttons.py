import pygame
pygame.init()


class Button:
    def __init__(self, text, x, y, wid, hei):
        self.maincolor = pygame.Color(0, 97, 100)
        self.butcolor = pygame.Color(0, 129, 132)
        self.nohov = pygame.Color(255, 255, 255)
        self.hov = pygame.Color(255, 255, 255)
        self.text = text
        self.x = x
        self.y = y
        self.wid = wid
        self.hei = hei

    def draw(self, window, hov=False):
        if hov:
            pygame.draw.rect(window, self.maincolor, (self.x, self.y, self.wid, self.hei), 0)
            pygame.draw.rect(window, self.hov, (self.x - 3, self.y - 3, self.wid + 6, self.hei + 6), 3)
            phrase = pygame.font.render(self.text, 1, (0, 0, 0))
            window.blit(phrase, (self.x + (self.wid / 2 - phrase.get_width() / 2),
                            self.y + (self.hei / 2 - phrase.get_height() / 2)))
        else:
            pygame.draw.rect(window, self.butcolor, (self.x, self.y, self.wid, self.hei), 0)
            pygame.draw.rect(window, self.nohov, (self.x - 3, self.y - 3, self.wid + 6, self.hei + 6), 3)
            phrase = pygame.font.render(self.text, 1, (0, 0, 0))
            window.blit(phrase, (self.x + (self.wid / 2 - phrase.get_width() / 2),
                                 self.y + (self.hei / 2 - phrase.get_height() / 2)))

    def onclick(self, pos):
        if self.x < pos[0] < self.x + self.wid:
            if self.y < pos[1] < self.y + self.hei:
                return True
        return False

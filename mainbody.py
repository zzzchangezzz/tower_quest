import pygame
import os
import sys
from buttons import Button
from helping_def import terminate, load_image
pygame.init()


class MenuWindow:
    def __init__(self):
        self.size = self.width, self.height = 640, 640
        self.butweight, self.butheight = 300, 80
        self.offset = 170
        self.space = 100
        self.titlspace = 140
        self.clr = pygame.Color(0, 97, 100)
        self.run = True

    def mainmenu(self):
        screen = pygame.display.set_mode(self.size)
        but_in_menu = []
        continue_but = Button('Продолжить', self.offset, self.titlspace)
        but_in_menu.append(continue_but)
        new_g_but = Button('Новая игра', self.offset, self.titlspace + self.space)
        but_in_menu.append(new_g_but)
        ach_but = Button('Достижения', self.offset, self.titlspace + self.space * 2)
        but_in_menu.append(ach_but)
        pre_but = Button('Предыстория', self.offset, self.titlspace + self.space * 3)
        but_in_menu.append(pre_but)
        exit_but = Button('Выход', self.offset, self.titlspace + self.space * 4)
        but_in_menu.append(exit_but)
        header = load_image('bigpic', 'title.png')
        while self.run:
            screen.fill(self.clr)
            screen.blit(header, (self.offset - 20, 11))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    terminate()
                if event.type == pygame.MOUSEMOTION:
                    for i in but_in_menu:
                        pos = pygame.mouse.get_pos()
                        i.set_hov(i.onclick(pos))
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if continue_but.onclick(pos):
                        # продолжить игру
                        pass
                    if new_g_but.onclick(pos):
                        # начать игру с первого уровня
                        pass
                    if ach_but.onclick(pos):
                        # показать достижения
                        pass
                    if pre_but.onclick(pos):
                        Prologue().tellstory()
                    if exit_but.onclick(pos):
                        terminate()
            for i in but_in_menu:
                i.draw(screen)
            pygame.display.flip()


class Prologue:
    def __init__(self):
        self.size = self.width, self.height = 640, 640
        self.curr_cadr = -1
        self.all_cadr = 4
        self.naming = 'P0.png'
        self.running = True

    def tellstory(self):
        screen = pygame.display.set_mode(self.size)
        while self.running:
            fon = pygame.transform.scale(load_image('prolog', self.naming), (self.width, self.height))
            screen.blit(fon, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    terminate()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.curr_cadr += 1
                    if self.curr_cadr > self.all_cadr:
                        self.running = False
                        return
                    else:
                        self.naming = 'P' + str(self.curr_cadr) + '.png'
                        fon = pygame.transform.scale(load_image('prolog', self.naming), (self.width, self.height))
                        screen.blit(fon, (0, 0))
            pygame.display.flip()


men = MenuWindow()
men.mainmenu()
pygame.quit()

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
                        self.run = False
                        return 'continue'
                    if new_g_but.onclick(pos):
                        self.run = False
                        return 'new game'
                    if ach_but.onclick(pos):
                        self.run = False
                        return 'achievements'
                    if pre_but.onclick(pos):
                        Prologue().tellstory()
                    if exit_but.onclick(pos):
                        self.run = False
                        return 'termination'
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


class Achievement:
    def __init__(self):
        self.size = self.width, self.height = 640, 640
        self.fill_clr = pygame.Color(0, 97, 100)
        self.txt_clr = pygame.Color(255, 255, 255)
        self.watch = True
        self.b_w, self.b_h = 128, 50
        self.back_button = Button('Назад', 24, 24, self.b_w, self.b_h)
        self.offset, self.ac_hei, self.leng = 60, 80, 500
        self.aff_one = 100
        ach_cod = []
        self.score = 0
        self.real_got = []
        with open("dostig.txt", encoding="utf-8") as ac:
            ach_cod = str(ac.read())
            ach_cod = ach_cod.split(',')
        for i in range(1, len(ach_cod)):
            if ach_cod[i] == 'T':
                if i == 1:
                    self.real_got.append('Начало положено. (Запустить игру, +10)')
                    self.score += 10
                if i == 2:
                    self.real_got.append('Путь к развитию. (Получена неплохая концовка, +150)')
                    self.score += 150
                if i == 3:
                    self.real_got.append('Восход. (Получена лучшая концовка, +300)')
                    self.score += 300
                if i == 4:
                    self.real_got.append('Пучина греха. (Получена худшая концовка, +100)')
                    self.score += 100

    def show_achievements(self):
        screen = pygame.display.set_mode(self.size)
        while self.watch:
            screen.fill(self.fill_clr)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.watch = False
                    return 'termination'
                if event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    self.back_button.set_hov(self.back_button.onclick(pos))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.back_button.onclick(pos):
                        self.watch = False
                        return 'menu'
                self.back_button.draw(screen)
                bit = 0
                fon = pygame.font.Font(None, 24)
                for j in range(len(self.real_got)):
                    n = j + 1
                    bit = n + 1
                    x = self.offset
                    y = self.aff_one * n
                    pygame.draw.rect(screen, self.txt_clr, (x, y, self.leng,
                                                            self.ac_hei), 3)
                    phr = fon.render(self.real_got[j], 1, self.txt_clr)
                    screen.blit(phr, (x + (self.leng / 2 - phr.get_width() / 2),
                                      y + (self.ac_hei / 2 - phr.get_height() / 2)))
                score_txt = 'Итого очков: ' + str(self.score)
                phr = fon.render(score_txt, 1, self.txt_clr)
                screen.blit(phr, (self.offset, self.aff_one * bit))
                pygame.display.flip()


class Finale():
    def __init__(self):
        pass
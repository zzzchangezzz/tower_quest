import pygame
import os
import sys
from buttons import Button
from mainbody import MenuWindow, Prologue, Achievement
from player import Player
from objects import Person, Tile, TurnTriangle, Chest
from helping_def import terminate, load_image
pygame.init()


def load_level(level, room):
    l_path = 'levels/' + str(level) + '/' + str(room) + '.txt'
    with open(l_path, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile(other_group, 'floor', x, y)
            elif level[y][x] == '0':
                Tile('wall0', x, y)
            elif level[y][x] == 'w':
                Tile(other_group, 'w', x, y)
            elif level[y][x] == 'a':
                Tile(other_group, 'a', x, y)
            elif level[y][x] == 's':
                Tile(other_group, 's', x, y)
            elif level[y][x] == 'd':
                Tile(other_group, 'd', x, y)
            elif level[y][x] == 'i':
                Tile(other_group, 'i', x, y)
            elif level[y][x] == 'e':
                Tile(other_group, 'e', x, y)
            elif level[y][x] == '#':
                Tile(front_exits, 'exit', x, y)
            elif level[y][x] == 'B':
                Tile(back_exits, 'exit', x, y)
            elif level[y][x] == '@':
                Tile(other_group, 'floor', x, y)
                new_player = Player(x, y)
    return new_player


f = open("savefile.txt", encoding="utf-8")
saving = f.read().split(',')
f.close()

current_level = int(saving[1])
current_room = 0
cards = []
for i in range(2, 5):
    cards.append(saving[i])

all_sprites = pygame.sprite.Group()
front_exits = pygame.sprite.Group()
back_exits = pygame.sprite.Group()
blocks = pygame.sprite.Group()
interactive = pygame.sprite.Group()
other_group = pygame.sprite.Group()

men = MenuWindow()
status = men.mainmenu()
while status == 'achievements':
    wind = Achievement()
    status = wind.show_achievements()
    if status == 'menu':
        men = MenuWindow()
        status = men.mainmenu()
if status == 'new game':
    saving[1] = '0'
    cards = []
    for i in range(2, 5):
        saving[i] = 'N'
        cards.append(saving[i])
    current_level = 0
    f = open("savefile.txt", "w", encoding="utf-8")
    f.write(','.join(saving))
    f.close()
    status = 'continue'
if status == 'continue':
    pass  # игра
if status == 'ending':
    pass  # класс показывания финала, запись достижения и сохранения, выход

if status == 'termination':
    terminate()

pygame.quit()

import pygame
import os
import sys
from buttons import Button
from mainbody import MenuWindow, Prologue
from player import Player
from objects import Person, Tile, TurnTriangle, Chest
from helping_def import terminate, load_image
pygame.init()

f = open("savefile.txt", encoding="utf-8")
saving = f.read().split(',')

current_level = saving[1]
cards = []
for i in range(2, 5):
    cards.append(saving[i])

men = MenuWindow()
status = men.mainmenu()
while status == 'achievements':
    pass  # достижения
if status == 'new game':
    pass  # перезаписание файла и статус 'continue'
if status == 'continue':
    pass  # игра
pygame.quit()

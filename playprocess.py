import pygame
import os
import sys
from buttons import Button
from mainbody import MenuWindow, Prologue, Achievement, Finale
from player import Player
from objects import Person, Tile, TurnTriangle, Chest, Exit
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
    for ly in range(len(level)):
        for lx in range(len(level[ly])):
            # Пустые блоки
            if level[ly][lx] == '.':
                Tile(other_group, 'floor', all_sprites,  lx, ly)
            elif level[ly][lx] == 'w':
                Tile(other_group, 'w', all_sprites, lx, ly)
            elif level[ly][lx] == 'a':
                Tile(other_group, 'a', all_sprites, lx, ly)
            elif level[ly][lx] == 's':
                Tile(other_group, 's', all_sprites, lx, ly)
            elif level[ly][lx] == 'd':
                Tile(other_group, 'd', all_sprites, lx, ly)
            elif level[ly][lx] == 'i':
                Tile(other_group, 'i', all_sprites, lx, ly)
            elif level[ly][lx] == 'e':
                Tile(other_group, 'e', all_sprites, lx, ly)

                # стены
            elif level[ly][lx] == '0':
                Tile(blocks, 'wall0', all_sprites, lx, ly)
            elif level[ly][lx] == '1':
                Tile(blocks, 'wall1', all_sprites, lx, ly)
            elif level[ly][lx] == '2':
                Tile(blocks, 'wall2', all_sprites, lx, ly)

                # выходы открытые
            elif level[ly][lx] == 'F':
                Exit(front_exits, all_sprites, 'front', lx, ly)
            elif level[ly][lx] == 'B':
                Exit(back_exits, all_sprites, 'back', lx, ly)
            elif level[ly][lx] == 'U':
                Exit(up_exits, all_sprites, 'up', lx, ly)
            elif level[ly][lx] == 'D':
                Exit(down_exits, all_sprites, 'down', lx, ly)

                # Выходы закрытые
            elif level[ly][lx] == 'N':
                Exit(unable_exits, all_sprites, 'down', lx, ly, False)
            elif level[ly][lx] == 'V':
                Exit(unable_exits, all_sprites, 'up', lx, ly, False)
            elif level[ly][lx] == 'P':
                Exit(unable_exits, all_sprites, 'front', lx, ly, False)
            elif level[ly][lx] == 'Z':
                Exit(unable_exits, all_sprites, 'back', lx, ly, False)

                # персоны
            elif level[ly][lx] == '@':
                Tile(other_group, 'floor', all_sprites,  lx, ly)
                new_player = Player(player_group, all_sprites, lx, ly)
            elif level[ly][lx] == 'C':
                Tile(other_group, 'floor', all_sprites,  lx, ly)
                Person(interactive, all_sprites, 'cult', cult_talk, lx, ly)
            elif level[ly][lx] == 'S':
                Tile(other_group, 'floor', all_sprites,  lx, ly)
                Person(interactive, all_sprites, 'sad', sad_talk, lx, ly)
            elif level[ly][lx] == 'L':
                Tile(other_group, 'floor', all_sprites,  lx, ly)
                Person(interactive, all_sprites, 'lazy', lazy_talk, lx, ly)

                # сундуки
            elif level[ly][lx] == '!':
                Chest(interactive, 'dark', all_sprites, lx, ly)
            elif level[ly][lx] == '?':
                Chest(interactive, 'light', all_sprites, lx, ly)

                # вращатели
            elif level[ly][lx] == '8':
                Tile(other_group, 'floor', all_sprites,  lx, ly)
                TurnTriangle(interactive, all_sprites, lx, ly, 0)
            elif level[ly][lx] == '6':
                Tile(other_group, 'floor', all_sprites,  lx, ly)
                TurnTriangle(interactive, all_sprites, lx, ly, 90)
            elif level[ly][lx] == '5':
                Tile(other_group, 'floor', all_sprites,  lx, ly)
                TurnTriangle(interactive, all_sprites, lx, ly, 180)
            elif level[ly][lx] == '4':
                Tile(other_group, 'floor', all_sprites,  lx, ly)
                TurnTriangle(interactive, all_sprites, lx, ly, 270)

    return new_player


f = open("savefile.txt", encoding="utf-8")
saving = f.read().split(',')
f.close()
max_level = 2

current_level = int(saving[1])
current_room = 0
cards = []
for i in range(2, 5):
    cards.append(saving[i])

all_sprites = pygame.sprite.Group()

front_exits = pygame.sprite.Group()
back_exits = pygame.sprite.Group()
down_exits = pygame.sprite.Group()
up_exits = pygame.sprite.Group()
unable_exits = pygame.sprite.Group()

blocks = pygame.sprite.Group()
interactive = pygame.sprite.Group()
player_group = pygame.sprite.Group()
other_group = pygame.sprite.Group()


cult_talk = False
lazy_talk = False
sad_talk = False
player = None
win_size = win_wid, win_hei = 640, 640
foncolr = pygame.Color(0, 0, 0)

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
    screen = pygame.display.set_mode(win_size)
    side_room = 0
    max_room = 4
    movement = None
    room_name = str(current_room) + '-' + str(side_room)
    player = generate_level(load_level(current_level, room_name))
    while status == 'continue':
        screen.fill(foncolr)
        e_press = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = 'termination'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    movement = 'left'
                    player.step(movement)
                elif event.key == pygame.K_d:
                    movement = 'right'
                    player.step(movement)
                elif event.key == pygame.K_w:
                    movement = 'up'
                    player.step(movement)
                elif event.key == pygame.K_s:
                    movement = 'down'
                    player.step(movement)
                elif event.key == pygame.K_e:
                    e_press = True
                    player.step(movement)
        if pygame.sprite.spritecollideany(player, blocks):
            player.back_step(movement)
        if pygame.sprite.spritecollideany(player, unable_exits):
            player.back_step(movement)
        if pygame.sprite.spritecollideany(player, interactive):
            player.back_step(movement)
        if e_press:
            player.step(movement)
            action_obj = pygame.sprite.spritecollideany(player, interactive)
            player.back_step(movement)
            if action_obj.obj_type() == 'triangle':
                action_obj.turn()

            if action_obj.obj_type() == 'person':
                if current_level == 0:
                    cult_talk = action_obj.talk(screen)
                if current_level == 1:
                    sad_talk = action_obj.talk(screen)
                if current_level == 2:
                    lazy_talk = action_obj.talk(screen)

            if action_obj.obj_type() == 'chest':
                taken, card = action_obj.take_mark(screen)
                if taken:
                    if card == 'light':
                        cards[current_level] = 'W'
                    elif card == 'dark':
                        cards[current_level] = 'B'
            open_exit = True
            tris = 0
            for obj in interactive:
                if obj.obj_type() == 'triangle':
                    tris += 0
                    angl = obj.return_angle()
                    if angl != 180:
                        open_exit = False
            if tris != 0 and open_exit:
                for ex in unable_exits:
                    s, direct, x, y = ex.return_stat()
                    ex.kill()
                    if direct == 'front':
                        nex_ex = Exit(front_exits, all_sprites, direct, x, y, True)
                    if direct == 'back':
                        nex_ex = Exit(back_exits, all_sprites, direct, x, y, True)
                    if direct == 'down':
                        nex_ex = Exit(down_exits, all_sprites, direct, x, y, True)
                    if direct == 'up':
                        nex_ex = Exit(up_exits, all_sprites, direct, x, y, True)
        if pygame.sprite.spritecollideany(player, front_exits):
            current_room += 1
            allow = True
            if current_room > max_room:
                alow = False
                if cards[current_level] != 'N':
                    current_level += 1
                    current_room = 0
                    allow = True
                    if current_level > max_level:
                        status = 'ending'

            if status == 'continue' and allow:
                for i in all_sprites:
                    i.kill()
                room_name = str(current_room) + '-' + str(side_room)
                player = generate_level(load_level(current_level, room_name))

        if pygame.sprite.spritecollideany(player, back_exits):
            current_room -= 1
            for i in all_sprites:
                i.kill()
            room_name = str(current_room) + '-' + str(side_room)
            player = generate_level(load_level(current_level, room_name))

        if pygame.sprite.spritecollideany(player, down_exits):
            side_room += 1
            for i in all_sprites:
                i.kill()
            room_name = str(current_room) + '-' + str(side_room)
            player = generate_level(load_level(current_level, room_name))

        if pygame.sprite.spritecollideany(player, up_exits):
            side_room -= 1
            for i in all_sprites:
                i.kill()
            room_name = str(current_room) + '-' + str(side_room)
            player = generate_level(load_level(current_level, room_name))

        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()


if status == 'ending':
    dark = 0
    light = 0
    for i in cards:
        if i == 'D':
            dark += 1
        if i == 'W':
            light += 1
    if dark > light:
        ends = Finale('bad')
        status = ends.showing()
    if dark < light < len(cards):
        ends = Finale('good')
        status = ends.showing()
    if light == len(cards):
        ends = Finale('best')
        status = ends.showing()

if status == 'termination':
    terminate()

terminate()

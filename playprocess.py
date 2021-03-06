import pygame
import os
import sys
from mainbody import MenuWindow, Achievement, Finale
from player import Player
from objects import Person, Tile, TurnTriangle, Chest, Exit
from helping_def import terminate

pygame.init()


def refresh_saving():  # запись файла сохранения на пустой
    saving[1] = '0'
    for i in range(2, 5):
        saving[i] = 'N'
    f = open("savefile.txt", "w", encoding="utf-8")
    f.write(','.join(saving))
    f.close()


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
                Tile(other_group, 'floor', all_sprites, lx, ly)
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
                blocks.add(Exit(unable_exits, all_sprites, 'down',
                                lx, ly, False))
            elif level[ly][lx] == 'V':
                blocks.add(Exit(unable_exits, all_sprites, 'up',
                                lx, ly, False))
            elif level[ly][lx] == 'P':
                blocks.add(Exit(unable_exits, all_sprites, 'front',
                                lx, ly, False))
            elif level[ly][lx] == 'Z':
                blocks.add(Exit(unable_exits, all_sprites, 'back',
                                lx, ly, False))

                # персоны
            elif level[ly][lx] == '@':
                Tile(other_group, 'floor', all_sprites, lx, ly)
                new_player = Player(player_group, all_sprites, lx, ly)
            elif level[ly][lx] == 'C':
                Tile(other_group, 'floor', all_sprites, lx, ly)
                Person(interactive, all_sprites, 'cult', cult_talk, lx, ly)
            elif level[ly][lx] == 'S':
                Tile(other_group, 'floor', all_sprites, lx, ly)
                Person(interactive, all_sprites, 'sad', sad_talk, lx, ly)
            elif level[ly][lx] == 'L':
                Tile(other_group, 'floor', all_sprites, lx, ly)
                Person(interactive, all_sprites, 'lazy', lazy_talk, lx, ly)

                # сундуки
            elif level[ly][lx] == '!':
                Chest(interactive, 'dark', all_sprites, lx, ly)
            elif level[ly][lx] == '?':
                Chest(interactive, 'light', all_sprites, lx, ly)

                # вращатели
            elif level[ly][lx] == '8':
                Tile(other_group, 'floor', all_sprites, lx, ly)
                TurnTriangle(interactive, all_sprites, lx, ly, 0)
            elif level[ly][lx] == '6':
                Tile(other_group, 'floor', all_sprites, lx, ly)
                TurnTriangle(interactive, all_sprites, lx, ly, 90)
            elif level[ly][lx] == '5':
                Tile(other_group, 'floor', all_sprites, lx, ly)
                TurnTriangle(interactive, all_sprites, lx, ly, 180)
            elif level[ly][lx] == '4':
                Tile(other_group, 'floor', all_sprites, lx, ly)
                TurnTriangle(interactive, all_sprites, lx, ly, 270)

    return new_player


pygame.key.set_repeat(200, 70)
f = open("savefile.txt", encoding="utf-8")
saving = f.read().split(',')
f.close()

current_level = int(saving[1])
current_room = 0
cards = []
for i in range(2, 5):
    cards.append(saving[i])

all_sprites = pygame.sprite.Group()
# группы выходов
front_exits = pygame.sprite.Group()
back_exits = pygame.sprite.Group()
down_exits = pygame.sprite.Group()
up_exits = pygame.sprite.Group()
unable_exits = pygame.sprite.Group()
# другие группы
blocks = pygame.sprite.Group()
interactive = pygame.sprite.Group()
player_group = pygame.sprite.Group()
other_group = pygame.sprite.Group()
# переменные
cult_talk = False
lazy_talk = False
sad_talk = False
player = None
max_level = 2
side_room = 0
max_room = 3
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

if status == 'new game':  # сохранение обнуляется и нидет основная игра
    refresh_saving()
    cards = []
    for i in range(2, 5):
        cards.append(saving[i])
    current_level = 0
    status = 'continue'

if status == 'continue':  # основная игра
    screen = pygame.display.set_mode(win_size)
    movement = None
    room_name = str(current_room) + '-' + str(side_room)
    player = generate_level(load_level(current_level, room_name))
    player.walls = blocks
    while status == 'continue':
        screen.fill(foncolr)
        e_press = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = 'termination'

            if event.type == event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_e:
                e_press = True

        player.move(pygame.key.get_pressed())
        player.updating()

        if e_press:  # Сигнал к взаимодействию
            action_obj = pygame.sprite.spritecollideany(player, interactive)
            if action_obj is not None:  # если есть с чем контактировать
                if action_obj.obj_type() == 'triangle':  # вращать
                    action_obj.turn()

                if action_obj.obj_type() == 'person':  # разговаривать
                    if current_level == 0:
                        cult_talk = action_obj.talk(screen, all_sprites,
                                                    player_group)
                    if current_level == 1:
                        sad_talk = action_obj.talk(screen, all_sprites,
                                                   player_group)
                    if current_level == 2:
                        lazy_talk = action_obj.talk(screen, all_sprites,
                                                    player_group)

                if action_obj.obj_type() == 'chest':  # открыть сундук
                    taken, card = action_obj.take_mark(screen, all_sprites,
                                                       player_group)
                    if taken:
                        if card == 'light':
                            cards[current_level] = 'W'
                        elif card == 'dark':
                            cards[current_level] = 'D'
            open_exit = True
            tris = 0
            for obj in interactive:
                if obj.obj_type() == 'triangle':
                    tris += 1
                    angl = obj.return_angle()
                    if angl != 180:
                        open_exit = False
            if tris != 0 and open_exit:  # ТОЛЬКО ДЛЯ УРОВНЯ С ВРАЩАТЕЛЕМ
                for ex in unable_exits:  # И ЗАКРЫТЫМИ ВЫХОДАМИ
                    s, direct, x, y = ex.return_stat()
                    ex.kill()
                    if direct == 'front':
                        nex_ex = Exit(front_exits, all_sprites, direct, x, y,
                                      True)
                    if direct == 'back':
                        nex_ex = Exit(back_exits, all_sprites, direct, x, y,
                                      True)
                    if direct == 'down':
                        nex_ex = Exit(down_exits, all_sprites, direct, x, y,
                                      True)
                    if direct == 'up':
                        nex_ex = Exit(up_exits, all_sprites, direct, x, y,
                                      True)
        if pygame.sprite.spritecollideany(player, front_exits):  # выход прямо
            allow = True
            if current_room + 1 > max_room:  # если финальный выход на уровне
                allow = False
                if cards[current_level] != 'N':  # если собрал метку
                    current_level += 1
                    current_room = 0
                    allow = True
                    if current_level > max_level:  # если всё прошел
                        status = 'ending'
                    else:
                        f = open("savefile.txt", "w", encoding="utf-8")
                        br = current_level - 1
                        saving[br + 2] = cards[br]
                        saving[1] = str(current_level)
                        f.write(','.join(saving))
                        f.close()
            else:
                current_room += 1
                allow = True

            if status == 'continue' and allow:  # если новая комната
                for i in all_sprites:
                    i.kill()
                room_name = str(current_room) + '-' + str(side_room)
                player = generate_level(load_level(current_level, room_name))
                player.walls = blocks

        if pygame.sprite.spritecollideany(player, back_exits):  # возвращение
            current_room -= 1
            for i in all_sprites:
                i.kill()
            room_name = str(current_room) + '-' + str(side_room)
            player = generate_level(load_level(current_level, room_name))
            player.walls = blocks

        if pygame.sprite.spritecollideany(player, down_exits):  # выход вниз
            side_room += 1
            for i in all_sprites:
                i.kill()
            room_name = str(current_room) + '-' + str(side_room)
            player = generate_level(load_level(current_level, room_name))
            player.walls = blocks

        if pygame.sprite.spritecollideany(player, up_exits):  # выход вверх
            side_room -= 1
            for i in all_sprites:
                i.kill()
            room_name = str(current_room) + '-' + str(side_room)
            player = generate_level(load_level(current_level, room_name))
            player.walls = blocks

        all_sprites.draw(screen)
        screen.blit(player.image, player.rect)
        # player_group.draw(screen)
        pygame.display.flip()

if status == 'ending':  # получение концовки
    dark = 0
    light = 0
    for i in cards:
        if i == 'D':
            dark += 1
        if i == 'W':
            light += 1
    with open("dostig.txt", encoding="utf-8") as ac:
        ach_update = str(ac.read()).split(',')
    ends = None
    if dark > light:  # худшая концовка
        ach_update[4] = 'T'
        ends = Finale('bad')
        status = ends.showing()

    if dark < light < len(cards):  # неплохая
        ach_update[2] = 'T'
        ends = Finale('good')
        status = ends.showing()

    if light == len(cards):  # лучшая
        ach_update[3] = 'T'
        ends = Finale('best')
        status = ends.showing()

    with open("dostig.txt", "w", encoding="utf-8") as f:
        f.write(','.join(ach_update))
    refresh_saving()

if status == 'termination':  # закрытие программы
    terminate()

terminate()

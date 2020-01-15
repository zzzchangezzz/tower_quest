import pygame
from helping_def import load_image, terminate


class Person(pygame.sprite.Sprite):
    def __init__(self, pers_group, all_sprites, name, talk, pos_x, pos_y):
        super().__init__(pers_group, all_sprites)
        pic_name = name + '.png'
        self.body = load_image('skin', pic_name, -1)
        self.emotions = []
        self.emotion = None
        self.name = name
        self.talked = talk
        for i in range(2):
            pic_name = 'em-' + name + '-' + str(i)
            self.emotions.append(load_image('skin', pic_name))
        self.dialog = []
        self.d_wid, self.d_hei = 640, 128
        self.d_x, self.d_y = 0, 512
        tile_size = 64
        self.rect = self.body.get_rect().move(tile_size * pos_x, tile_size * pos_y)
        self.dialog_rect = pygame.Surface([self.d_wid, self.d_hei])

    def talk(self, screen):
        self.dialog = self.set_dialog()
        for i in range(len(self.dialog)):
            self.emotion = self.emotions[i % 2]
            font = pygame.font.Font(None, 18)
            phras = self.dialog[i]
            self.dialog_rect.fill(pygame.Color(0, 0, 0))
            screen.blit(self.dialog_rect, (self.d_x, self.d_y))
            screen.blit(self.emotion, (512, 512))
            told = font.render(phras, 1, (255, 255, 255))
            screen.blit(told, (10, 530))
            pygame.display.flip()
            while pygame.event.wait().type != pygame.KEYDOWN:
                pass
        return self.talked

    def set_dialog(self):
        phr = []
        if self.name == 'cult':
            if not self.talked:
                phr.append('Здравствуйте! Вижу, Вы попали в Башню.')
                phr.append('Что ж, возможно, вы не самый праведный человек.')
                phr.append('Вам нужно собрать метки. Их два вида - темные и светлые.')
                phr.append('Светлые тяжелее собрать. Но я бы не советовал брать темные.')
                phr.append('Впрочем, это ваше решение. Без метки вы не можете пройти на следующий этаж.')
                phr.append('Решайте головоломки, и сможете получить светлые метки.')
                phr.append('А можете просто собрать темные. Их легче получить.')
                phr.append('Актуальна лишь последняя взятая марка. Удачи!')
                self.talked = True
            if self.talked:
                phr.append('Что-то не ясно?')
                phr.append('Собери все метки решая загадки и искупи вину перед Башней!')
                phr.append('Удачи.')

        if self.name == 'lazy':
            if not self.talked:
                phr.append('Кто-то дошёл сюда? Ты, кажется, решителен!')
                phr.append('Мне уже лень искать все эти метки.')
                phr.append('Кто эти загадки вообще выдумал?')
                phr.append('Может останешься со мной?')
                self.talked = True
            if self.talked:
                phr.append('Всё-таки хочешь поболтать?')
                phr.append('А ты не такая решительная, как я думал!')
                phr.append('Да ну, я пошутил.')

        if self.name == 'sad':
            if not self.talked:
                phr.append('Ох, кто-то ещё здесь?')
                phr.append('Рада, что кто-то еще смог пройти тот этаж.')
                phr.append('Но я не могу пройти дальше.')
                phr.append('Для светлой метки нужно пройти лабиринт, но я боюсь в него идти.')
                phr.append('А вдруг я потеряюсь в нем?')
                phr.append('Если сможешь пройти его, поделишься светлой меткой?')
                self.talked = True
            if self.talked:
                phr.append('Что-то еще? Кстати, я тут подумала...')
                phr.append('Оставь метку себе. Лучше просто скажи, как пройти лабиринт.')
        return phr

    def obj_type(self):
        return 'person'


class Tile(pygame.sprite.Sprite):
    def __init__(self, sprite_group, tag, all_sprites, pos_x, pos_y):
        super().__init__(sprite_group, all_sprites)
        self.image = load_image('bigpic', tag + '.png')
        self.tag = tag
        tile_size = 64
        self.rect = self.image.get_rect().move(tile_size * pos_x, tile_size * pos_y)


class TurnTriangle(pygame.sprite.Sprite):
    def __init__(self, sprite_group, all_sprites, pos_x, pos_y, angl):
        super().__init__(sprite_group, all_sprites)
        self.angle = angl
        img = 'tri-' + str(self.angle) + '.png'
        self.image = load_image('bigpic', img, -1)
        tile_size = 64
        self.rect = self.image.get_rect().move(tile_size * pos_x, tile_size * pos_y)

    def turn(self):
        self.angle += 90
        if self.angle == 360:
            self.angle = 0
        img = 'tri-' + str(self.angle) + '.png'
        self.image = load_image('bigpic', img, -1)

    def return_angle(self):
        return self.angle

    def obj_type(self):
        return 'triangle'


class Chest(pygame.sprite.Sprite):
    def __init__(self, sprite_group, tag, all_sprites, pos_x, pos_y):
        super().__init__(sprite_group, all_sprites)
        self.mark = tag
        self.image = load_image('bigpic', 'chest.png')
        tile_size = 64
        self.rect = self.image.get_rect().move(tile_size * pos_x, tile_size * pos_y)
        self.speak_wind = pygame.Surface([640, 64])

    def take_mark(self, screen):
        p = ''
        take = False
        if self.mark == 'dark':
            p = 'В сундуке темная марка. Взять? (Q - да, W - нет)'
        if self.mark == 'light':
            p = 'В сундуке светлая марка. Взять? (Q - да, W - нет)'
        font = pygame.font.Font(None, 18)
        self.speak_wind.fill(pygame.Color(0, 0, 0))
        screen.blit(self.speak_wind, (0, 576))
        inf = font.render(p, 1, (255, 255, 255))
        screen.blit(inf, (5, 580))
        answer = False
        pygame.display.flip()
        while not answer:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        answer = True
                    if event.key == pygame.K_q:
                        take = True
                        answer = True
        if take:
            self.speak_wind.fill(pygame.Color(0, 0, 0))
            screen.blit(self.speak_wind, (0, 576))
            p = 'Вы взяли метку.'
            inf = font.render(p, 1, (255, 255, 255))
            screen.blit(inf, (5, 580))
            pygame.display.flip()
        return take, self.mark

    def obj_type(self):
        return 'chest'


class Exit(pygame.sprite.Sprite):
    def __init__(self, sprite_group, all_sprites, direct, pos_x, pos_y, active=True):
        super().__init__(sprite_group, all_sprites)
        self.direction = direct
        self.status = active
        self.image = load_image('bigpic', 'exit.png')
        if not self.status:
            self.image = load_image('bigpic', 'unable.png')
        tile_size = 64
        self.x, self.y = pos_x, pos_y
        self.rect = self.image.get_rect().move(tile_size * pos_x, tile_size * pos_y)

    def return_stat(self):
        return self.status, self.direction, self.x, self.y

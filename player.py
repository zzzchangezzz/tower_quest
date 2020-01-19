import pygame
from helping_def import load_image


class Player(pygame.sprite.Sprite):
    def __init__(self, player_group, all_sprites, pos_x, pos_y, walls=[]):
        super().__init__(player_group, all_sprites)
        self.image = load_image('skin', 'player.png', -1)
        self.tile_size = 64

        self.walls = walls

        self.x, self.y = pos_x, pos_y
        self.rect = self.image.get_rect().move(self.tile_size * pos_x, self.tile_size * pos_y)
        self.step = 1
        self.cur_frame = 0
        self.frames = []

        self.direction = "down"

        self.runRightImages = self.cut_sheet(load_image('skin', 'right.png', -1), 4, 1)
        self.runLeftImages = self.cut_sheet(load_image('skin', 'left.png', -1), 4, 1)
        self.runUpImages = self.cut_sheet(load_image('skin', 'up.png', -1), 4, 1)
        self.runDownImages = self.cut_sheet(load_image('skin', 'down.png', -1), 4, 1)

        self.pauseAnim = 0.2
        self.getTicksLastFrame = pygame.time.get_ticks()

        self.yvel = 0
        self.xvel = 0

        self.last_way = None
        self.cur_way = None

    def move(self, keys):
        if not (keys[pygame.K_d] or keys[pygame.K_a]):  # стоим, когда нет указаний идти
            self.xvel = 0

        if not (keys[pygame.K_w] or keys[pygame.K_s]):
            self.yvel = 0

        if keys[pygame.K_d]:
            self.xvel = self.step
            self.direction = "right"

        elif keys[pygame.K_a]:
            self.xvel = -self.step
            self.direction = "left"

        elif keys[pygame.K_w]:
            self.yvel = -self.step
            self.direction = "up"

        elif keys[pygame.K_s]:
            self.yvel = self.step
            self.direction = "down"

        self.rect.y += self.yvel
        self.collides(0, self.yvel, self.walls)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collides(self.xvel, 0, self.walls)

        if self.direction == "right":
            self.frames = self.runRightImages
        elif self.direction == "left":
            self.frames = self.runLeftImages
        elif self.direction == "up":
            self.frames = self.runUpImages
        elif self.direction == "down":
            self.frames = self.runDownImages

    def collides(self, xvel, yvel, platforms):
        for prefab in platforms:
            if pygame.sprite.collide_rect(self, prefab):  # если есть пересечение платформы с игроком
                if xvel > 0:  # если движется вправо
                    self.rect.right = prefab.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = prefab.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = prefab.rect.top  # то не падает вниз
                    # self.yvel = 0  # анимация остановится и не будет биться в стену

                if yvel < 0:  # если движется вверх
                    self.rect.top = prefab.rect.bottom  # то не движется вверх
                    # self.yvel = 0  # анимация остановится и не будет биться в стену

    def cut_sheet(self, sheet, columns, rows):
        frames = []
        width_step, height_step = sheet.get_width() // columns, sheet.get_height() // rows
        rect = pygame.Rect(0, 0, width_step, height_step)
        for j in range(rows):
            for i in range(columns):
                frame_location = (width_step * i, width_step * j)
                frames.append(sheet.subsurface(pygame.Rect(frame_location, rect.size)))
        return frames

    def updating(self):
        self.pauseAnim -= (pygame.time.get_ticks() - self.getTicksLastFrame) / 1500.0

        if (self.pauseAnim <= 0):
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.pauseAnim = 0.1

        if (self.xvel == 0 and self.yvel == 0):
            self.image = self.frames[0]

        self.getTicksLastFrame = pygame.time.get_ticks()

    def get_pos(self):
        return self.rect.x, self.rect.y

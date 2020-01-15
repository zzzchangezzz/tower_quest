import pygame
from helping_def import load_image


class Player(pygame.sprite.Sprite):
    def __init__(self, player_group, all_sprites, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image('skin', 'player.png', -1)
        tile_size = 64
        self.rect = self.image.get_rect().move(tile_size * pos_x + 15, tile_size * pos_y + 5)
        self.step = 16
        self.cur_frame = 0
        self.iter_num = 0
        self.frames = []
        self.last_way = None
        self.cur_way = None

    def moving_player(self, direction):
        self.cur_way = direction
        if self.cur_way != self.last_way:
            picture = direction + '.png'
            self.refresh_iteration(picture)
        self.updating()
        self.last_way = self.cur_way
        if direction == 'up':
            self.rect.y -= self.step
        if direction == 'down':
            self.rect.y += self.step
        if direction == 'left':
            self.rect.x -= self.step
        if direction == 'right':
            self.rect.x += self.step

    def back_step(self, front_dir):
        if front_dir == 'up':
            self.rect.y += self.step
        if front_dir == 'down':
            self.rect.y -= self.step
        if front_dir == 'left':
            self.rect.x += self.step
        if front_dir == 'right':
            self.rect.x -= self.step

    def refresh_iteration(self, pict):
        self.iter_num = 0
        self.cur_frame = 0
        self.cut_sheet(load_image('skin', pict, -1), 4, 1)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames = []
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def updating(self):
        self.iter_num += 1
        if self.iter_num > 4:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.iter_num = 0

    def get_pos(self):
        return self.rect.x, self.rect.y

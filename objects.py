import pygame
from helping_def import load_image


class Person(pygame.sprite.Sprite):
    def __init__(self, pers_group, all_sprites, name, pos_x, pos_y):
        super().__init__(pers_group, all_sprites)
        pic_name = name + '.png'
        self.body = load_image('skin', pic_name, -1)
        self.emotions = []
        for i in range(2):
            pic_name = 'em_' + name + '_' + str(i)
            self.emotions.append(load_image('skin', pic_name))
        self.dialog = []
        self.d_wid, self.d_hei = 640, 224
        self.d_x, self.d_y = 0, 416
        tile_size = 64
        self.rect = self.body.get_rect().move(tile_size * pos_x, tile_size * pos_y)

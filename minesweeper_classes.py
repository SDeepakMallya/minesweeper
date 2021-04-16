#!/usr/bin/env python3

import pygame



def load_image(path):
    try:
        image = pygame.image.load(path)
    except pygame.error as message:
        print("Cannot load image:", name)
        raise SystemExit(message)
    image = image.convert()
    return image



class Cells(pygame.sprite.Sprite):
    """
    Sprite class for cells
    """

    def __init__(self, pos, value=0, state=1):
        pygame.sprite.Sprite.__init__(self)

        self.state = state    # 0 for Closed cell, 1 for open, 2 for flagged
        self.__value = value        # Default: Closed cell (-1 for mine, 0-8 otherwise)
        img_src = './images/closed.png'      # Closed cell
        self.image = load_image(img_src)

        self.rect = self.image.get_rect()
        self.rect.center = pos      # Set position of cell'
        self.ruin = False


    def get_value(self):
        if self.state == 1:     # Only allow reading cell value when it is open
            return self.__value
        else:
            return None

    def set_value(self, value):
        self.__value = value

    def open_sesame(self):
        if self.__value >= 0:
            img_src = './images/type{}.png'.format(self.__value)
        else:
            img_src = './images/mine_red.png'
            self.ruin = True
        self.image = load_image(img_src)
        self.state = 1

    def flag(self):
        img_src = './images/flag.png'
        self.image = load_image(img_src)
        self.state = 2

    def unflag(self):
        img_src = './images/closed.png'
        self.image = load_image(img_src)
        self.state = 0

    def update(self, click):
        # self.open_sesame()
        if self.rect.collidepoint(click.pos):
            if self.state == 0:
                if click.button == 1:
                    self.open_sesame()
                elif click.button == 3:
                    self.flag()
            elif self.state == 2 and click.button == 3:
                self.unflag()

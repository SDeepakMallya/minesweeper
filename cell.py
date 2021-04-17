#!/usr/bin/env python3

import pygame

CELL_WIDTH = 20
CELL_HEIGHT = 20

def load_image(path):
    try:
        image = pygame.image.load(path)
    except pygame.error as message:
        print("Cannot load image:", path)
        raise SystemExit(message)
    image = image.convert()
    return image



class Cell(pygame.sprite.Sprite):
    """
    Sprite class for cells
    """

    def __init__(self, pos, value=0, state=1):
        pygame.sprite.Sprite.__init__(self)

        self.state = state    # 0 for Closed cell, 1 for open, 2 for flagged
        self.__value = value        # Default: (-1 for mine, 0-8 otherwise)
        img_src = './images/closed.png'      # Closed cell
        self.image = load_image(img_src)

        self.rect = self.image.get_rect()
        self.rect.center = [pos[0] * CELL_WIDTH + CELL_WIDTH//2, pos[1] * CELL_HEIGHT + CELL_HEIGHT//2]      # Set position of cell
        self.ruin = False


    def get_value(self):
        if self.state == 1:     # Only allow reading cell value when it is open
            return self.__value
        else:
            return None

    def get_state(self):
        return self.state

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
        if self.state == 0:
            if click.button == 1:
                self.open_sesame()
            elif click.button == 3:
                self.flag()
        elif self.state == 2 and click.button == 3:
            self.unflag()


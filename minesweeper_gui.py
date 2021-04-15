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

class Right_Side_Panel:

    def __init__(self):
        pass


class Cells(pygame.sprite.Sprite):
    """
    Sprite class for cells
    """

    def __init__(self, pos, ind=0, state=0):
        pygame.sprite.Sprite.__init__(self)

        self.state = state    # 0 for Closed cell (default), 1 for open, 2 for flagged
        self.__ind = ind        # Default: Closed cell (-1 for mine, 0-8 otherwise)
        img_src = './Images/closed.png'      # Closed cell
        self.image = load_image(img_src)

        self.rect = self.image.get_rect()
        self.rect.center = pos      # Set position of cell


    def get_ind(self):
        if self.state == 1:     # Only allow reading cell ind when it is open
            return self.__ind
        else:
            return None

    def open_sesame(self):
        if self.__ind >= 0:
            img_src = './Images/type%d.png' %(self.__ind)
        else:
            img_src = './Images/mine.png'
        self.image = load_image(img_src)
        self.state = 1

    def flag(self):
        img_src = './Images/flag.png'
        self.image = load_image(img_src)
        self.state = 2

    def unflag(self):
        img_src = './Images/closed.png'
        self.image = load_image(img_src)
        self.state = 0


    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    if self.state == 0:
                        if event.button == 1:
                            self.open_sesame()
                        elif event.button == 3:
                            self.flag()
                    elif self.state == 2 and event.button == 3:
                        self.unflag()

#!/usr/bin/env python3

from minesweeper_gui import Cells
import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((700, 700))
    pygame.display.set_caption('Minesweeper')

    clock = pygame.time.Clock()
    fps = 50

    cell = Cells([400, 200], 4, 0)
    cell.move = [pygame.K_LEFT, pygame.K_RIGHT]

    cell_group = pygame.sprite.Group()
    cell_group.add(cell)

    while True:
        key = pygame.key.get_pressed()
        if key[cell.move[0]]:
            cell.open_sesame()
        elif key[cell.move[1]]:
            cell.flag_it()

        cell_group.draw(screen)

        pygame.display.update()
        clock.tick(fps)

        # Gathering event information
        event_list = pygame.event.get()
        cell_group.update(event_list)

        # Check for exit signal
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                return

if __name__ == '__main__':
    main()

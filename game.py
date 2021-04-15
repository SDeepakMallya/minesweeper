#!/usr/bin/env python3

from minesweeper_classes import Cells
import pygame

CELL_WIDTH = 20
CELL_HEIGHT = 20

def set_board(rows, cols):
    """
    Set up bard based on rows and columns
    """
    cell_group = pygame.sprite.Group()
    cell_centers = []
    for r in range(cols):
        col_centers = []
        rc = r * CELL_HEIGHT + CELL_HEIGHT//2
        for c in range(rows):
            center = [rc, c * CELL_WIDTH + CELL_HEIGHT//2]
            cell_group.add(Cells(center))
            col_centers.append(center)
        cell_centers.append(col_centers)
    return cell_group, cell_centers

def set_mines(cell_group, first_click):
    """
    Place mines and populate cells
    """


def main():
    pygame.init()
    screen = pygame.display.set_mode((700, 700))
    pygame.display.set_caption('Minesweeper')

    clock = pygame.time.Clock()
    fps = 50

    rows, cols = 16, 30

    board, cell_id = set_board(rows, cols)

    # cell = Cells([400, 200], 4, 0)

    while True:
        board.draw(screen)

        pygame.display.update()
        clock.tick(fps)

        # Gathering event information
        event_list = pygame.event.get()


        # Check for exit signal
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            else:
                board.update(event_list)

if __name__ == '__main__':
    main()

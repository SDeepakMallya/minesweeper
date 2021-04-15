#!/usr/bin/env python3

from minesweeper_gui import Cells
import pygame


def set_board(rows, cols):
    """
    Set up bard based on rows and columns
    """
    cell_group = pygame.sprite.Group()
    cell_centers = []
    for r in range(rows):
        col_centers = []
        rc = r*20 + 10
        for c in range(cols):
            center = [rc, c*20 + 10]
            cell_group.add(Cells(center, 4, 0))
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
        board.update(event_list)

        # Check for exit signal
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                return

if __name__ == '__main__':
    main()

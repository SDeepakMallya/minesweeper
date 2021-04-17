#!/usr/bin/env python3

from cell import Cell
import math
import pygame
import random

CELL_WIDTH = 20
CELL_HEIGHT = 20

ADJ = [(i, j) for i in [-1, 0, 1] for j in [-1, 0, 1]]

def get_loc_from_pos(pos):
    """
    Get location in grid from position
    """
    loc  = [math.floor(pos[1])//CELL_HEIGHT, math.floor(pos[0])//CELL_WIDTH]
    return loc


class Game:

    def __init__(self, rows, cols, mines):
        self.cell_group = []
        self.mine_locations = random.sample(range(rows*cols), mines)
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.mines_remaining = mines

        for loc in range(rows*cols):
            c, r = loc%cols, loc//cols
            center = [c, r]
            if loc in self.mine_locations:
                self.cell_group.append(Cell(center, value = -1, state = 0))
            else:
                neighbour_mines = 0
                for k in ADJ:
                    nei = [c + k[0], r + k[1]]
                    if nei[0] >= 0 and nei[0] < cols and nei[1] >= 0 and nei[1] < cols:
                        loc_1d = nei[0] + nei[1] * cols
                        if loc_1d in self.mine_locations:
                            neighbour_mines += 1
                self.cell_group.append(Cell(center, value = neighbour_mines, state = 0))

    def open_all_neighbours(self, loc):
        """
        Open neighbouring cells if the value is same as flags in neighbourhood
        """

        loc_1d = loc[0] + loc[1] * self.cols
        if self.cell_group[loc_1d].get_state() == 1:
            count_flagged = 0
            for k in ADJ:
                nei = [loc[0] + k[0], loc[1] + k[1]]
                if nei[0] >= 0 and nei[0] < self.cols and nei[1] >= 0 and nei[1] < self.cols:
                    nei_1d = nei[0] + nei[1] * self.cols
                    if self.cell_group[nei_1d].get_state() == 2:
                        count_flagged += 1

            if count_flagged == self.cell_group[loc_1d].get_value():
                for k in ADJ:
                    nei = [loc[0] + k[0], loc[1] + k[1]]
                    if nei[0] >= 0 and nei[0] < self.cols and nei[1] >= 0 and nei[1] < self.cols:
                        nei_1d = nei[0] + nei[1] * self.cols
                        self.cell_group[nei_1d].open_sesame()
                        if self.cell_group[nei_1d].get_value() == 0:
                            self.blank_encounter(nei)



    def blank_encounter(self, loc):
        """
        Clicking on empty cell opens all the neighbouring cells
        """

        for k in ADJ:
            nei = [loc[0] + k[0], loc[1] + k[1]]
            if nei[0] >= 0 and nei[0] < self.cols and nei[1] >= 0 and nei[1] < self.cols:
                nei_1d = nei[0] + nei[1] * self.cols
                if self.cell_group[nei_1d].get_state() == 0:
                    self.cell_group[nei_1d].open_sesame()
                    if self.cell_group[nei_1d].get_value() == 0:
                        self.blank_encounter(nei)


# def set_board(ROWS, COLS):
#     """
#     Set up board based on ROWS and columns
#     """
#     cell_group = pygame.sprite.Group()
#     cell_id = []
#     for r in range(ROWS):
#         col_id = []
#         rc = r * CELL_HEIGHT + CELL_HEIGHT//2
#         for c in range(COLS):
#             center = [c * CELL_WIDTH + CELL_WIDTH//2, rc]
#             cell = Cell(center)
#             cell_group.add(cell)
#             col_id.append(cell)
#         cell_id.append(col_id)
#     return cell_group, cell_id





# def set_mines(cell_id, mine_count=10):
#     """
#     Place mines and populate cells
#     """
#     mine_pos = []
#     for count in range(mine_count):
#         mr, mc = random.randint(0, ROWS-1), random.randint(0, COLS-1)
#         cell_id[mr][mc].set_value(-1)

#     # # Count number of mines in neighbouring cells
#     for r in range(ROWS):
#         for c in range(COLS):
#             if cell_id[r][c].get_value() != -1:
#                 count = 0
#                 for k in ADJ:
#                     x, y = r + k[0], c + k[1]
#                     if x >= 0 and x < ROWS and y >= 0 and y < COLS:
#                         if cell_id[x][y].get_value() == -1:
#                             count += 1
#                 cell_id[r][c].set_value(count)

#     # Set state of cells to closed (0)
#     for r in range(ROWS):
#         for c in range(COLS):
#             cell_id[r][c].state = 0




# def blank_encounter(cell_id, loc_x, loc_y):
#     """
#     Open all neighbouring cells when a blank cell is encountered
#     """
#     # adj = [(i, j) for i in [-1, 0, 1] for j in [-1, 0, 1]]
#     for k in ADJ:
#         x, y = loc_x + k[0], loc_y + k[1]
#         if x >= 0 and x < ROWS and y >= 0 and y < COLS:     # Check bounds on location
#             if cell_id[x][y].state == 0:    # Check if cell is closed (prevents infinite recursion)
#                 cell_id[x][y].open_sesame()
#                 if cell_id[x][y].get_value() == 0:
#                     blank_encounter(cell_id, x, y)


# def open_neighbours(cell_id, loc_x, loc_y):
#     """
#     Open all unflagged neighbouring cells if number of flagged neighbours matches cell value
#     """
#     if cell_id[loc_x][loc_y].state != 1:      # Execute code only when cell is open
#         return

#     count_flagged = 0
#     for k in ADJ:
#         x, y = loc_x + k[0], loc_y + k[1]
#         if x >= 0 and x < ROWS and y >= 0 and y < COLS: # Check bounds on location
#             if cell_id[x][y].state == 2:
#                 count_flagged += 1
#     if cell_id[loc_x][loc_y].get_value() == count_flagged:
#         for k in ADJ:
#             x, y = loc_x + k[0], loc_y + k[1]
#             if x >= 0 and x < ROWS and y >= 0 and y < COLS:
#                 if cell_id[x][y].state == 0:        # Check if cell is closed
#                     cell_id[x][y].open_sesame()
#                     if cell_id[x][y].get_value() == 0:
#                         blank_encounter(cell_id, x, y)


def main():
    pygame.init()
    screen = pygame.display.set_mode((700, 700))
    pygame.display.set_caption('Minesweeper')

    clock = pygame.time.Clock()
    fps = 50

    ROWS, COLS = 16, 30

    board, cell_id = set_board(ROWS, COLS)
    set_mines(cell_id, 99)

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                board.update(event)
                button = event.button
                print("Button pressed: ", button)
                mouse_pos = event.pos
                x, y = get_loc_from_pos(mouse_pos)

                # Check if x, y correspond to a grid location
                if x < ROWS and y < COLS and cell_id[x][y].state == 1:
                    if button == 1:
                        if cell_id[x][y].get_value() == 0:
                            blank_encounter(cell_id, x, y)  #
                        elif cell_id[x][y].ruin:
                            print("BETTER LUCK IN NEXT JANM")
                            pygame.quit()
                            return
                    if button == 2:
                        open_neighbours(cell_id, x, y)
                        # Incorporate game end on opening mine


if __name__ == '__main__':
    main()

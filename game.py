#!/usr/bin/env python3


import math
import random
import pygame

from cell import Cell

ADJ = [(i, j) for i in [-1, 0, 1] for j in [-1, 0, 1]]

class Game:

    def __init__(self, rows, cols, mines):
        self.cell_group = pygame.sprite.Group()
        self.cell_list = []
        self.mine_locations = random.sample(range(rows*cols), mines)
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.mines_remaining = mines
        self.game_on = True
        self.cells_remaining = self.rows * self.cols - self.mines

        for loc in range(rows*cols):
            c, r = int(loc%cols), int(loc//cols)
            center = [c, r]
            if loc in self.mine_locations:
                cell = Cell(center, value = -1, state = 0)
                self.cell_list.append(cell)
                self.cell_group.add(cell)
            else:
                neighbour_mines = 0
                for k in ADJ:
                    nei = [r + k[0], c + k[1]]
                    if nei[0] >= 0 and nei[0] < rows and nei[1] >= 0 and nei[1] < cols:
                        loc_1d = nei[0] * self.cols + nei[1] 
                        if loc_1d in self.mine_locations:
                            neighbour_mines += 1
                cell = Cell(center, value = neighbour_mines, state = 0)
                self.cell_list.append(cell)
                self.cell_group.add(cell)

    def open_all_neighbours(self, loc):
        """
        Open neighbouring cells if the value is same as flags in neighbourhood
        """

        changed_cells = []
        loc_1d = loc[0] * self.cols + loc[1]
        if self.cell_list[loc_1d].get_state() == 1:
            count_flagged = 0
            for k in ADJ:
                nei = [loc[0] + k[0], loc[1] + k[1]]
                if nei[0] >= 0 and nei[0] < self.rows and nei[1] >= 0 and nei[1] < self.cols:
                    nei_1d = nei[0] * self.cols + nei[1]
                    if self.cell_list[nei_1d].get_state() == 2:
                        count_flagged += 1

            if count_flagged == self.cell_list[loc_1d].get_value():
                for k in ADJ:
                    nei = [loc[0] + k[0], loc[1] + k[1]]
                    if nei[0] >= 0 and nei[0] < self.rows and nei[1] >= 0 and nei[1] < self.cols:
                        nei_1d = nei[0] * self.cols + nei[1]
                        if self.cell_list[nei_1d].get_state() == 0:
                            self.cell_list[nei_1d].open_sesame()
                            changed_cells.append(self.cell_list[nei_1d])
                            if self.cell_list[nei_1d].get_value() == 0:
                                changed_cells += self.blank_encounter(nei)
        return changed_cells


    def blank_encounter(self, loc):
        """
        Clicking on empty cell opens all the neighbouring cells
        """
        changed_cells = []
        for k in ADJ:
            nei = [loc[0] + k[0], loc[1] + k[1]]
            if nei[0] >= 0 and nei[0] < self.rows and nei[1] >= 0 and nei[1] < self.cols:
                nei_1d = nei[0] * self.cols + nei[1]
                if self.cell_list[nei_1d].get_state() == 0:
                    self.cell_list[nei_1d].open_sesame()
                    changed_cells.append(self.cell_list[nei_1d])
                    if self.cell_list[nei_1d].get_value() == 0:
                        changed_cells += self.blank_encounter(nei)
        return changed_cells
    
    def play(self, loc, button):
        changed_cells = []
        loc_1d = int(loc[0] * self.cols + loc[1])

        if button == 1:
            if self.cell_list[loc_1d].get_state() == 0:
                self.cell_list[loc_1d].open_sesame()
                changed_cells.append(self.cell_list[loc_1d])

            if self.cell_list[loc_1d].get_value() == 0:
                changed_cells += self.blank_encounter(loc)
            
            if self.cell_list[loc_1d].get_value() == -1:
                self.game_on = False
            
            self.cells_remaining -= len(changed_cells)
        
        elif button == 2:
            changed_cells += self.open_all_neighbours(loc)
            self.cells_remaining -= len(changed_cells)

        elif button == 3:
            if self.cell_list[loc_1d].get_state() == 0:
                self.cell_list[loc_1d].flag()
                self.mines_remaining -= 1
                changed_cells.append(self.cell_list[loc_1d])

            elif self.cell_list[loc_1d].get_state() == 2:
                self.cell_list[loc_1d].unflag()
                self.mines_remaining += 1
                changed_cells.append(self.cell_list[loc_1d])
        
        return changed_cells

            

 


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
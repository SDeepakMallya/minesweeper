#!/usr/bin/env python3

import random
import pygame

from cell import Cell, Counter

ADJ = [(i, j) for i in [-1, 0, 1] for j in [-1, 0, 1]]

class Game:

    def __init__(self, rows, cols, mines, offset):
        self.cell_group = pygame.sprite.Group()
        self.cell_list = []
        self.mine_locations = random.sample(range(rows*cols), mines)
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.mines_remaining = mines
        self.game_on = True
        self.cells_remaining = self.rows * self.cols - self.mines
        self.clock = pygame.sprite.Group()
        self.mine_counter = pygame.sprite.Group()

        for digit in [0, 1, 2]:
            pos = [cols - 2 - digit*0.75, 1.5]
            clock_digit = Counter(pos, digit)
            self.clock.add(clock_digit)

        for digit in [0, 1]:
            pos = [1 - digit*0.75, 1.5]
            mine_digit = Counter(pos, digit)
            self.mine_counter.add(mine_digit)

        for loc in range(rows*cols):
            c, r = int(loc % cols), int(loc // cols)
            center = [c, r]
            if loc in self.mine_locations:
                cell = Cell(center, ind = loc, value = -1, state = 0)
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
                cell = Cell(center, ind = loc, value = neighbour_mines, state = 0, shift = offset)
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
                changed_cells = self.blank_encounter(loc)
        return changed_cells


    def blank_encounter(self, loc):
        """
        Opens unflagged neighbouring cells
        """
        changed_cells = []
        for k in ADJ:
            nei = [loc[0] + k[0], loc[1] + k[1]]
            if nei[0] >= 0 and nei[0] < self.rows and nei[1] >= 0 and nei[1] < self.cols:
                nei_1d = nei[0] * self.cols + nei[1]
                if self.cell_list[nei_1d].get_state() == 0:
                    self.cell_list[nei_1d].open_sesame()
                    if self.cell_list[nei_1d].get_value() == -1:
                        self.game_on = False
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

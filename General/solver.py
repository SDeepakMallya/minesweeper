#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Implementing a solver for Minesweeper deployable online
"""

import numpy as np
import sympy # For RREF calculation (can be done without)
import time

def sure_shot(board, mine_counts):
    state = (np.concatenate((board, mine_counts), axis=1))
    rref, pivots = sympy.Matrix(state).rref() # Write your own code here.
    loc = [] # Stores list of locations and corresponding mine value in tuples

    for i in range(len(pivots)):
        # for j in range(0, len(pivots)):
        #     if rref[j, pivots[i]] == 1:
        #         if np.count_nonzero(rref[j, :-1]) == 1:
        #             loc.append((pivots[i], rref[j, -1]))
        #             print("Location: %d, Mine: " %(pivots[i]), rref[j, -1])
        #         prev = j
        if np.count_nonzero(rref[i, :-1]) == 1:
            loc.append((pivots[i], rref[i, -1]))
            print("Location: %d, Mine: " %(pivots[i]), rref[i, -1])
    return loc

if __name__ == '__main__':

    r, c = (9, 8)

    # Setting up the board
    mines = [1,1,0,1,1,1,1,2,2]
    R = np.array(mines).reshape(r, 1)
    P = np.zeros((r,c))
    loc = [(0, 2), (0, 3), (1, 3), (2, 3), (3, 3),
           (5, 2), (5, 2), (6, 2), (6, 2)]
    for i in range(r):
        start, count = loc[i]
        for j in range(count):
            P[i, start + j] = 1
    #P[8, 10] = 1
    print("J: ",j)
    print("Board \n", P.shape)
    print("Mine vector \n", R.shape)
    known_mines = sure_shot(P, R)
    print("Known mines: ", known_mines)





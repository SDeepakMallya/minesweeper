#!/usr/bin/env python3

import math
import pygame

from game import Game

CELL_WIDTH = 20
CELL_HEIGHT = 20

WINDOW_HEIGHT = 700
WINDOW_WIDTH = 700

def get_loc_from_pos(pos):
    """
    Get location in grid from position
    """
    loc  = [math.floor(pos[1])//CELL_HEIGHT, math.floor(pos[0])//CELL_WIDTH]
    return loc

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Minesweeper')

    clock = pygame.time.Clock()
    fps = 50

    #ADD INPUT WIDGETS
    rows, cols, mines = 16, 30, 99

    game = Game(rows, cols, mines)
    game.cell_group.draw(screen)
    print("Here")
    pygame.display.update()

    while True:
        changed_cells = []
        # pygame.display.update()
        clock.tick(fps)

        # Gathering event information
        event_list = pygame.event.get()

        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                button = event.button
                # print("Button pressed: ", button)
                mouse_pos = event.pos
                loc = get_loc_from_pos(mouse_pos)
                # print("Clicked Cell: {}".format(loc))
                if loc[0] < rows and loc[1] < cols:
                    changed_rects =  [cell.rect for cell in game.play(loc, button)]

                
                if not game.game_on:
                    print ("Better Luck Next Time.")
                    print ("Mines Remaining: {}, Cells Remaining: {}".format(game.mines_remaining, game.cells_remaining))

                    pygame.quit()
                    return
                
                elif not game.mines_remaining:
                    print ("Congrats! You flagged all the mines!")

                    pygame.quit()
                    return

                elif not game.cells_remaining:
                    print ("Congrats! You cleared the board!")

                    pygame.quit()
                    return

                else:
                    print ("Mines Remaining: {}, Cells Remaining: {}".format(game.mines_remaining, game.cells_remaining))
      
        #TO DO: restrict update to just changed cells
        game.cell_group.draw(screen)
        pygame.display.update(changed_rects)            
        
if __name__ == '__main__':
    main()

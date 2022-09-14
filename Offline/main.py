#!/usr/bin/env python3

import math
import pygame

from game import Game

CELL_WIDTH = 20
CELL_HEIGHT = 20

WINDOW_HEIGHT = 700
WINDOW_WIDTH = 700

def get_loc_from_pos(pos, offset=3):
    """
    Get location in grid from position
    """
    loc  = [math.floor(pos[1])//CELL_HEIGHT - offset, math.floor(pos[0])//CELL_WIDTH]
    return loc

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Minesweeper')

    clock = pygame.time.Clock()
    fps = 50
    offset = 3

    #ADD INPUT WIDGETS
    rows, cols, mines = 16, 30, 99

    game = Game(rows, cols, mines, offset)
    game.cell_group.draw(screen)
    game.clock.draw(screen)
    game.mine_counter.draw(screen)

    print("Here")
    pygame.display.update()

    start = False
    run_time = 0
    while True:
        changed_cells = []
        changed_rects = None
        # pygame.display.update()
        clock.tick(fps)

        # Gathering event information
        event_list = pygame.event.get()

        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not start:
                    run_time = 0    # Set clock to 0 at first click
                    start = True

                button = event.button
                # print("Button pressed: ", button)
                mouse_pos = event.pos
                loc = get_loc_from_pos(mouse_pos, offset)
                # print("Clicked Cell: {}".format(loc))
                if loc[0] < rows and loc[1] < cols and loc[0] >= 0:
                    changed_cells = game.play(loc, button)
                    changed_rects =  [cell.rect for cell in changed_cells]

                if not game.game_on:
                    print ("Better Luck Next Time.")
                    print ("Mines Remaining: {}, Cells Remaining: {}".format(game.mines_remaining, game.cells_remaining))
                    pygame.quit()
                    return

                # This exit condition is meaningless as one can just place mines randomly and make the mines_remaining = 0
                # elif not game.mines_remaining:
                #     print ("Congrats! You flagged all the mines!")
                #     pygame.quit()
                #     return


                elif not game.cells_remaining:
                    print ("Congrats! You cleared the board!")
                    pygame.quit()
                    return

                else:
                    game.mine_counter.update(game.mines_remaining)
                    print ("Mines Remaining: {}, Cells Remaining: {}".format(game.mines_remaining, game.cells_remaining))

        if start:       # Run the clock after start
            run_time += clock.get_time()/1000
            if run_time > 999:
                run_time = 999
                print("Stop wasting my time!!!")
            game.clock.update(math.floor(run_time))

        #TO DO: restrict update to just changed cells
        game.cell_group.draw(screen)
        game.clock.draw(screen)
        game.mine_counter.draw(screen)
        # pygame.display.update(changed_rects)
        pygame.display.update()


if __name__ == '__main__':
    main()

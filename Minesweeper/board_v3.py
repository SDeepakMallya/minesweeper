from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import numpy as np
import sweeper
import time


def initiate(driver, mode='expert'):
    # driver.find_element(By.ID, 'options-link').click()
    # game = driver.find_element(By.ID, 'options-form')
    # game.find_element(By.ID, mode).click()
    # game.submit()
    slate = driver.find_element(By.ID, 'game')
    return slate


def gen_cell_objects(mine_space, rows, cols):
    """
    Stores handles for the cells in a 2D array
    """
    cells = []
    for i in range(rows):
        cells.append([])
        for j in range(cols):
            elem = mine_space.find_element(By.ID, "cell_%d_%d" %(j, i))
            cells[i].append(elem)
    return cells


def get_cell_value(elem):
    """
    Assigns appropriate value after reading cell
    Based on the syntax of http://minesweeperonline.com
    """
    val = elem.get_attribute('class')[-1]
    if val == 'd':  # Covered Cell
        val = -1
    elif val == 'd': # Flagged (Currently not used)
        val = -2
    elif val == '1':
        if elem.get_attribute('class')[-2] == '1':
            val = -3     # Mine, used continuing with a guess
        else:
            val = int(val)

    else:
        val = int(val)
    return val


# @sweeper.timer
def read_data(cells, data):
    """
    Populates data by reading cells
    """
    rows, cols = len(cells), len(cells[0])
    for i in range(rows):
        for j in range(cols):
            if data[i][j] == -1:
                elem = cells[i][j]
                data[i][j] = get_cell_value(elem)
    return data


# @sweeper.timer
def read_data_rev(cells, data):
    """
    Read data from cells and indicate boundary cells
    """
    rows, cols = len(cells), len(cells[0])
    update_bdry = []
    for i in range(rows):
        for j in range(cols):
            if data[i][j] == -1:
                elem = cells[i][j]
                val = get_cell_value(elem)
                data[i][j] = val
                if val > 0:
                    nb = (i, j)
                    update_bdry.append(nb)
    return data, update_bdry


def elem_index(arr, elem):
    """
    Returns index of elem if present in the list arr
    and None otherwise
    """
    try:
        ind = arr.index(elem)
        return ind
    except ValueError:
        return None

def flag_cell(cell, act):
    """
    Flag the cell
    This site support ctrl+click for flagging
    """
    # Simulate right click or ctrl+click using selenium
    ctrl = Keys.CONTROL
    # act.key_down(ctrl).click(cell).key_up(ctrl).perform()
    cell.context_click()


def add_constraint(pos, A, b, locs, data, adjs):
    """
    Add constraint based on the cell located at 'pos'
    """
    rows, cols = len(data), len(data[0])
    x, y = pos
    x_ind = []  # List of indices of adjacent cells
    new_locs = 0    # Counters for new covered cells
    dim_x = len(locs)   # Current dimension of variables
    val = data[x][y]
    for k in adjs:
        adj_x, adj_y = x + k[0], y + k[1]
        if adj_x < 0 or adj_x >= rows or adj_y < 0 or adj_y >= cols:
            continue
        if data[adj_x][adj_y] == -2:
            val -= 1
            continue
        if data[adj_x][adj_y] == -1:
            pos = (adj_x, adj_y)
            ind = elem_index(locs, pos)
            if ind is not None:
                x_ind.append(ind)
            else:
                locs.append(pos)
                new_locs += 1
                x_ind.append(dim_x)
                dim_x += 1

    if len(x_ind) == 0:
        # This case does not add any new information
        # All the adjacent cells are either mines or open
        pass
    else:
        new_row = np.zeros((1, dim_x))
        new_row[0, x_ind] = 1
        if b.size > 0:
            zero_pad = np.zeros((b.size, new_locs))
            A = np.concatenate((A, zero_pad), axis=1)
            A = np.concatenate((A, new_row))
        else:
            A = new_row
        b = np.insert(b, b.size, val)
    return A, b, locs


# @sweeper.timer
def problem_formulation(data):
    """
    Generates A, b and x (locs) from data
    """
    rows, cols = len(data), len(data[0])
    A = np.array([])
    b = np.array([])
    locs = []
    adjs = [(i, j) for i in [-1,0,1] for j in [-1,0,1]]
    for i in range(rows):
        for j in range(cols):
            val = data[i][j]
            if val > 0:
                pos = (i, j)
                A, b, locs = add_constraint(pos, A, b, locs, data, adjs)
    return A, b, locs


# @sweeper.timer
def problem_formulation_rev(data, bdry):
    rows, cols = len(data), len(data[0])
    A = np.array([])
    b = np.array([])
    locs = []
    adjs = [(i, j) for i in [-1,0,1] for j in [-1,0,1]]
    for pos in bdry:
        A, b, locs = add_constraint(pos, A, b, locs, data, adjs)
    return A, b, locs


# @sweeper.timer
def solve4locations(alpha, beta, guess, tol=1e-3):
    """
    Obtain info about mine/safe locations
    """
    sol_x, succ = sweeper.ipm4mines(alpha, beta)
    if not succ:
        raise RuntimeError('Linprog failed')
    # sol_x = sweeper.MineProbs(alpha, beta)
    mines = []
    safe = []

    for i in range(len(sol_x)):
        if abs(sol_x[i] - 1) < tol:
            mines.append(i)
        elif abs(sol_x[i]) < tol:
            safe.append(i)

    # Guessing Incorporated (almost random)
    if len(safe) == 0:
        print('No safe cells')
        if guess:
                safest = np.argmin(sol_x)  # Almost random picking
                safe.append(safest)
        else:
            ask = input('Continue with a guess:(y/n)')
            if ask == 'y':
                safest = np.argmin(sol_x)  # Almost random picking
                safe.append(safest)

    return mines, safe

# @sweeper.timer
def update_data(mine_locs, safe_locs, cells, data):
    """
    Click safe cells, flag mines and update data
    """
    enc_blank = False
    for sl in safe_locs:
        x, y = sl
        # print("Clicking at ", sl)
        cells[x][y].click()
        val = get_cell_value(cells[x][y])
        data[x][y] = val
        if val == 0:
            enc_blank = True # Checks encounter with blank cells
        elif val == -3:
            return data, False, True

    for ml in mine_locs:
        x, y = ml
        # cells[x][y].context_click() # Flag the cell
        # flag_cell(cells[x][y], action)
        data[x][y] = -2     # Flag the cell
    return data, enc_blank, False

# @sweeper.timer
def update_problem(A, b, locs, data, adjs, mines, safe):
    """
    Update A, b, locs with new constraints
    """
    mine_locs = [locs[m] for m in mines]
    safe_locs = [locs[s] for s in safe]
    for m in mines:
        b -= A[:, m]

    for kl in safe_locs + mine_locs:
        locs.remove(kl)
    A = np.delete(A, mines + safe, axis=1)

    # Handling redundant rows
    red_rows = [l for l in range(b.size) if b[l] == 0]

    A = np.delete(A, red_rows, axis=0)
    b = np.delete(b, red_rows)

    for sl in safe_locs:
        A, b, locs = add_constraint(sl, A, b, locs, data, adjs)
    return A, b, locs


def total_mine_constraint():
    """
    Incorporate total mine count constraint
    """
    # To be implemented
    pass


def solve_board(cells, data, tot_mines, guess):
    """
    Deterministic solving, no guessing incorporated
    tot_mines denotes the total mines in the board
    """
    xyz = time.time()
    data = read_data(cells, data)
    A, b, locs = problem_formulation(data)
    adjs = [(i, j) for i in [-1,0,1] for j in [-1,0,1]]
    mine_count = 0
    ipm_tol = 1e-2

    iter_start = time.time()
    while True:
        print("Problem size: ", A.shape, tot_mines - mine_count)

        mines, safe = solve4locations(A, b, guess, ipm_tol)
        mine_count += len(mines)
        if len(safe) == 0:
            return mine_count, False

        # Update step
        mine_locs = [locs[m] for m in mines]
        safe_locs = [locs[s] for s in safe]
        data, flag, dead = update_data(mine_locs, safe_locs, cells, data)

        if mine_count == tot_mines: # Break Condition
            break

        if dead:
            print("Better luck next time")
            return mine_count, False
        # if tot_mines - mine_count < 10:
            # Add total_mine_constraint
            # A, b, locs = total_mine_constraint()
            # pass

        if flag:    # Encountered a blank cell
            data = read_data(cells, data)
            A, b, locs = problem_formulation(data)

            # Alternate update rule (Has some bugs).
            # Reduces redundannt calculations but
            # no significant improvement in runtime on expert mode

            # data, bdry = read_data_rev(cells, data)
            # A, b, locs = update_problem(A, b, locs, data, adjs, mines, safe)
            # bdry_ind = []
            # for pos in bdry:
            #     ind = elem_index(locs, pos)
            #     if ind is not None:
            #         bdry_ind.append(ind)
            #     A = np.delete(A, bdry_ind, axis=1)
            #     A, b, locs = add_constraint(pos, A, b, locs, data, adjs)
        else:
            A, b, locs = update_problem(A, b, locs, data, adjs, mines, safe)

        iter_end = time.time()
        # print("Iteration time: ", iter_end - iter_start)
    return mine_count, True

def solver_time(game):
    """
    Reads the timer from the website http://minesweeperonline.com
    """
    timer = 0
    timer_cell = ['1', '10', '100']
    weights = [1, 10, 100]
    for t in range(3):
        w = game.find_element(By.ID, 'top_area_time_' + timer_cell[t])
        digit = w.get_attribute('class')[-1]
        timer += int(digit)*weights[t]
    return timer


def start_game(browser, mode='intermediate', attempt=0):
    """
    Starts the game and keeps restarting until solved without guesses
    """
    mine_space = initiate(browser, mode)
    global action
    action = ActionChains(browser)
    hwm = {'beginner': [9, 9, 10], 'intermediate': [16, 16, 40],
           'expert': [16, 30, 99]}
    rows, cols, tot_mines = hwm[mode]

    face = mine_space.find_element(By.ID, 'top_area_face')
    cells = gen_cell_objects(mine_space, rows, cols)

    retry = 'y'
    while retry == 'y':
        attempt += 1
        guess_flag = input("Proceed with guesses when required automatically?:(y/n) ")
        if guess_flag == 'y':
            guess = True
        else:
            guess = False
        # Reset board
        data = [[-1 for j in range(cols)] for i in range(rows)]
        face.click()
        status = True
        # x, y = input("Location:")
        x, y = np.random.randint(rows), np.random.randint(cols)
        x = int(x)
        y = int(y)
        print(cells[x][y].get_attribute('id'))
        start_sig = input("Start now")
        attempt_start = time.time()
        cells[x][y].click()
        # data, bdry = new_read_data(cells, data)
        try:
            mines_found, status = solve_board(cells, data, tot_mines, guess)
            attempt_end = time.time()
        except UnexpectedAlertPresentException as err:
            attempt_end = time.time()
            # attempt_dur = solver_time(mine_space)
            print("Success at attempt %d under time %d \t %f" %(attempt, attempt_dur, attempt_end - attempt_start))
        if not status:
            # attempt_dur = solver_time(mine_space)
            print("Cannot proceed without a guess\nRemaining mines:  %d" %(tot_mines - mines_found))
            # print("Elapsed time: %d \t %f" %(attempt_dur, attempt_end - attempt_start))
            # try:
            #     pred_time = tot_mines*attempt_dur/mines_found
            #     print("Predicted time: %f" %(tot_mines*attempt_dur/mines_found))
            # except ZeroDivisionError:
            #     print("You found nothing")
        retry = input("Try again?:(y/n)")


if __name__ == '__main__':

    opt = webdriver.FirefoxOptions()
    opt.add_argument("--private")

    browser = webdriver.Chrome(executable_path='/home/sdeepakmallya/chromedriver')

    # browser = webdriver.Chrome(executable_path=r'./chromedriver96')

    browser.get('https://minesweeper.online/new-game')
    mode = 'intermediate'
    mode = input('Mode (beginner/intermediate/expert):')
    from importlib import reload # For Testing purposes
    game = browser.find_element(By.ID, 'game')
    start_game(browser, mode)

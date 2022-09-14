from selenium import webdriver
import numpy as np
import sweeper


def get_cell_value(elem):
    val = elem.get_attribute("class")[-1]
    if val == 'k':
        val = -1
    elif val != 'd':
        val = int(val)
    else:
        val = -2
    return val

def initiate(driver, mode="expert"):
    driver.find_element_by_id("options-link").click()
    game = driver.find_element_by_id("options-form")
    game.find_element_by_id(mode).click()
    game.submit()
    slate = driver.find_element_by_id("game")
    return slate


def gen_cell_objects(board, mode="beginner"):
    cells = []
    data = []
    if mode == "expert":
        rows, cols = 16, 30
    elif mode == "intermediate":
        rows, cols = 16, 16
    else:
        rows, cols = 9, 9

    for i in range(rows):
        cells.append([])
        data.append([])
        for j in range(cols):
            elem = board.find_element_by_id("%d_%d" %(i+1, j+1))
            cells[i].append(elem)
            val = get_cell_value(elem)
            data[i].append(val)
    return cells, data

def read_data(cells):
    rows, cols = len(cells), len(cells[0])
    data =  []
    for i in range(rows):
        data.append([])
        for j in range(cols):
            elem = cells[i][j]
            val = get_cell_value(elem)
            data[i].append(val)
    return data

def elem_ind(arr, elem):
    try:
        ind = arr.index(elem)
        return ind
    except ValueError:
        return None

def add_constraint(pos, A, b, locs, data, adjs):
    rows, cols = len(data), len(data[0])
    x, y = pos
    x_ind = []
    new_locs = 0
    dim_x = len(locs)
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
            ind = elem_ind(locs, pos)
            if ind is not None:
                x_ind.append(ind)
            else:
                locs.append(pos)
                new_locs += 1
                x_ind.append(dim_x)
                dim_x += 1
    if True:
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

def prob_form(data):
    rows, cols = len(data), len(data[0])
    A = np.array([])
    b = np.array([])
    locs = []
    # dim_x = 0
    adjs = [(i, j) for i in [-1,0,1] for j in [-1,0,1]]
    for i in range(rows):
        for j in range(cols):
            val = data[i][j]
            if val > 0:
                pos = (i, j)
                A, b, locs = add_constraint(pos, A, b, locs, data, adjs)
                # x_ind = []
                # new_locs = 0
                # for k in adjs:
                #     adj_x, adj_y = i + k[0], j + k[1]
                #     if adj_x < 0 or adj_x >= rows or adj_y < 0 or adj_y >= cols:
                #         continue
                #     if data[adj_x][adj_y] == -2:
                #         val -= 1
                #         continue
                #     if data[adj_x][adj_y] == -1:
                #         pos = (adj_x, adj_y)
                #         ind = elem_ind(locs, pos)
                #         if ind is not None:
                #             x_ind.append(ind)
                #         else:
                #             locs.append(pos)
                #             new_locs += 1
                #             x_ind.append(dim_x)
                #             dim_x += 1
                # new_col = np.zeros((dim_x, 1))
                # new_col[x_ind] = 1
                # if b.size > 0:
                #     zero_pad = np.zeros((new_locs, b.size))
                #     A = np.concatenate((A, zero_pad))
                #     A = np.concatenate((A, new_col), axis=1)
                # else:
                #     A = new_col
                # b = b.insert(b, b.size, val)

    return A, b, locs



def update_on_click(x, y, data, cells):
    elem = cells[x][y]
    elem.click()
    val = get_cell_value(elem)

    if val > 0:
        data[x][y] = val
    elif val == 0:
        data = read_data(cells)


def start_game(browser, mode='beginner'):
    board = initiate(browser, mode)
    cells, data = gen_cell_objects(board, mode)
    rows, cols = len(cells), len(cells[0])
    face = board.find_element_by_id("face")

    x, y = np.random.randint(rows), np.random.randint(cols)
    cells[x][y].click()

    data = read_data(cells)
    A, b, locs = prob_form(data)
    adjs = [(i, j) for i in [-1,0,1] for j in [-1,0,1]]
    mine_count = 0
    tol = 5e-2
    if mode == 'beginner':
        lim = 10
    elif mode == 'intermediate':
        lim = 40
    elif mode == 'expert':
        lim = 99

    while mine_count <= lim:
        print("Mines left: ", lim - mine_count)
        sol_x = sweeper.ipm4mines(A, b)
        mines = []
        flag = False
        safe = []
        for i in range(sol_x.size):
            if abs(sol_x[i] - 1) < tol:
                mines.append(i)
                mine_count += 1
            elif abs(sol_x[i]) < tol:
                safe.append(i)
        if len(safe) == 0:
            print("No safe locations")
            data = read_data(cells)
            A, b, locs = prob_form(data)
            mine_count = 0
            continue
            # print(A, b, locs)
            # print(sol_x)
            # absol = sweeper.MineProbs(A, b)
            # print(absol)
            # break

        for s in safe:
            x, y = locs[s]
            cells[x][y].click()
            val = get_cell_value(cells[x][y])
            if val == 0:
                flag = True
            data[x][y] = val

        for m in mines:
            x, y = locs[m]
            # cells[x][y].context_click()
            data[x][y] = -2


        # mine_locs = []
        # for m in mines:
        #      b -= A[:, m]
        #      mine_locs.append(locs[m])

        # A = np.delete(A, mines, axis=1)
        # for ml in mine_locs:
        #     locs.remove(ml)

        # for l in range(b.size):
        #     if b[l] == 0:
        #         for m in range(A.shape[1]):
        #             if A[l, m] == 1:
        #                 x, y = locs[m]
        #                 cells[x][y].click()


        # print("Preparing board")
        # A, b, locs = prob_form(data)

        if flag:
            print("Regenerating Data")
            A, b, locs = prob_form(data)
        else:
            for m in mines:
                b -= A[:, m]

            mine_locs = [locs[m] for m in mines]
            safe_locs = [locs[s] for s in safe]
            for kl in safe_locs + mine_locs:
                locs.remove(kl)
            A = np.delete(A, mines + safe, axis=1)

            red_rows = [l for l in range(b.size) if b[l] == 0]
            red_locs = []
            red_cols = []
            for l in red_rows:
                for m in range(A.shape[1]):
                    if A[l, m] == 1:
                        red_locs.append(locs[m])
                        red_cols.append(m)
            for rl in red_locs:
                x, y = rl
                cells[x][y].click()
                data[x][y] = get_cell_value(cells[x][y])
                locs.remove(rl)
            A = np.delete(A, red_cols, axis=1)
            A = np.delete(A, red_rows, axis=0)
            b = np.delete(b, red_rows)

            # for l in range(b.size):
            #     if b[l] == 0:
            #         # for m in range(A.shape[1]):
            #         #     if A[l, m] == 1:
            #         #         x, y = locs[m]
            #         #         cells[x][y].click()
            #         #         data[x][y] = get_cell_value(cells[x][y])
            #         #         locs.remove(locs[m])
            #         A = np.delete(A, l, axis=0)
            #         b = np.delete(b, l)

            for sl in safe_locs + red_locs:
                A, b, locs = add_constraint(sl, A, b, locs, data, adjs)





if __name__ == '__main__':

    opt = webdriver.FirefoxOptions()
    opt.add_argument("--private")

    driver = webdriver.Firefox(executable_path=r'./geckodriver',
                            firefox_options=opt)
    driver.get('http://minesweeperonline.com/')
    mode = 'expert'

    start_game(driver, 'intermediate')

import numpy as np
import cvxopt
import constraint
import scipy.optimize as sciopt
import time


def timer(func):
    def wrapper(*args, **kwargs):
        now = time.process_time()
        res = func(*args, **kwargs)
        print("Time by %s: %f" %(func.__name__, time.process_time() - now))
        return res
    return wrapper


def forwardSub(P, q):
    rows = q.size
    sol = np.zeros(rows)
    sol[0] = q[0]/P[0, 0]
    for i in range(1, rows):
        val = q[i]
        for j in range(i):
            val -= P[i, j]*sol[j]
        sol[i] = val/P[i, i]
    return sol

@timer
def pinv4mines(A, b, samples=1):
    dim = A.shape[1]
    beta = np.linalg.pinv(A)
    res = np.zeros(dim)
    for k in range(samples):
        center = np.random.rand(dim)
        if samples == 1:
            center = 0.5*np.ones(dim)
        disp = b - np.dot(A, center)
        sol = center + np.dot(beta, disp)
        res += sol

    return res/samples


@timer
def qr4mines(A, b, samples=1):
    cols = A.shape[1]
    q, r = np.linalg.qr(A.T)
    res = np.zeros(cols)
    for k in range(samples):
        center = np.random.rand(cols)
        if samples == 1:
            center = 0.5*np.ones(cols)
        disp = b - np.dot(A, center)
        ln_sol = forwardSub(r.T, disp)
        sol = center + np.dot(q, ln_sol)
        res += sol
    return res/samples


@timer
def cvx4mines(A, b):
    rows, cols = A.shape
    eye = np.eye(cols)
    cent = np.ones(cols)
    P = cvxopt.matrix(eye)
    c = cvxopt.matrix(-0.5*cent)
    Q = cvxopt.matrix(A)
    r = cvxopt.matrix(b)
    doeye = np.concatenate((eye, -eye))
    h = np.concatenate((cent, np.zeros(cols)))
    G = cvxopt.matrix(doeye)
    l = cvxopt.matrix(h)
    cvxopt.solvers.options['show_progress'] = False
    cvx = cvxopt.solvers.qp(P, c, G, l, Q, r)
    return cvx['x']


# @timer
def ipm4mines(A, b, meth='interior-point'):
    dim = A.shape[1]
    center = np.zeros(dim)
    sol = sciopt.linprog(center, A_eq=A, b_eq=b,
                         bounds=(0, 1), method=meth)
    sol_x = sol['x']
    success = sol['success']
    return sol_x, success


@timer
def MineProbs(A, b):
    show = constraint.Problem()
    rows, cols = A.shape
    var = range(cols)
    show.addVariables(var, [0, 1])
    for i in range(rows):
        pres = []
        for j in range(cols):
            if A[i, j] == 1:
                pres.append(var[j])
        show.addConstraint(constraint.ExactSumConstraint(b[i]), pres)
    possibilities = show.getSolutions()
    tot_pos = len(possibilities)
    probs = []
    for i in range(cols):
        tot = 0
        for pos in possibilities:
            tot += pos[i]
        probs.append(tot/tot_pos)
    return probs


def printer(pinv, qr, cvx, prob, ipm):
    dim = len(prob)
    print("\nPosition: \t   PINV \t\tQR \t \t  CVXOPT \t     IPM \tProbability")
    for i in range(dim):
        print("   %d:    \t %f \t %f \t %f \t  %f \t %f" %(i+1, pinv[i], qr[i], cvx[i], ipm[i],prob[i]))
    print("\n")


def compareMines(A, b, samples=1):
    pinv = pinv4mines(A, b, samples)
    qr = qr4mines(A, b, samples)
    cvx = cvx4mines(A, b)
    ipm, suc = ipm4mines(A, b, 'interior-point')
    probs = MineProbs(A, b)
    printer(pinv, qr, cvx, probs, ipm)

if __name__ == '__main__':
    omega =    np.array([[1.0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1]]) # Matrix A
    counts = np.array([3.0,3,3,1,2,1,3,1]) # Vector B

    A = np.zeros((44,53))
    A[0][:2] = 1
    A[1][:3] = 1
    A[2][1:4] = 1
    A[3][2:6] = 1
    A[4][5] = 1
    A[5][5:7]= 1
    A[6][5:8] = 1
    A[7][6:9] = 1
    A[8][7:10] =1
    A[9][8:12] =1
    A[10][11] =1
    A[11][11:13]=1
    A[12][11:16]=1
    A[13][14:17]=1
    A[14][15:18]=1
    A[15][16:19]=1
    A[16][17:20]=1
    A[17][18:23]=1
    A[18][21:24]=1
    A[19][22:25]=1
    A[20][23:28]=1
    A[21][26:29]=1
    A[22][27:29]=1
    A[23][28]=1
    A[24][28:31]=1
    A[25][29]=1
    A[26][29:33]=1
    A[27][31:34]=1
    A[28][32:35]=1
    A[29][33:36]=1
    A[30][34:38]=1
    A[31][37]=1
    A[32][37:40]=1
    A[33][39]=1
    A[34][39:41]=1
    A[35][39:44]=1
    A[36][42:45]=1
    A[37][43:46]=1
    A[38][44:47]=1
    A[39][45:50]=1
    A[40][48:51]=1
    A[41][49:]=1
    A[41][0]=1
    A[42][-1]=1
    A[42][0]=1
    A[43][0]=1

    B = np.array([1.0,2,1,3,1,1,1,1,1,2,1,1,2,2,2,2,2,2,1,1,3,2,2,1,2,1,1,1,1,1,1,1,2,1,1,2,1,1,1,2,1,1,1,1])
    compareMines(A, B, 10)
    compareMines(omega, counts, 10)
    # expt()


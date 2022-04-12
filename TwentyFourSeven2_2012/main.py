import time
import numpy as np
from TwentyFourSevenSolver import TwentyFourSevenSolver
from scipy.ndimage import label

import logging
logging.basicConfig(filename='tewntyfourseven2.log', filemode='w',
    level=logging.INFO,
    format='[%(levelname)s] %(message)s')

import data


def checkView(V, view, side):
    N, _ = V.shape
    # left and top views just see head of row/col
    if side == "l" or side == "t":
        head = 0
    # right and bot views just see tail of row/col
    elif side == "r" or side == "b":
        head = -1
    else:
        raise 

    # top and bottom look at columns, i.e. transposed rows
    if side == "t" or side == "b":
        V = V.T

    for it, vt in view:
        i = np.where(V[it])[0][head]
        if vt != V[it,i]:
            return False
    return True        

def findSolution(vals_list, views, find_all_solutions=False):
    tstart = time.time()
    TFSSolver = TwentyFourSevenSolver(vals_list, **views, find_all_solutions=find_all_solutions)
    solutions = []
    Ys = []
    for vals, _, Y in TFSSolver.solutions:
            solutions.append(vals)
            Ys.append(Y)
            break
    if not solutions:
        return None
    return (solutions[0], Ys[0]) if not find_all_solutions else (solutions, Ys)


def main1(vals_list=data.vals_list_1, views=data.views_1):
    '''
    Used to drive a particular instance
    '''
    tstart = time.time()
    sol = findSolution(vals_list, views, find_all_solutions=False)
    print(f'Total time: {(time.time() - tstart)*1000: .2f}ms')

    if sol is None:
        print('NO SOLUTION FOUND')
        return None
    s1, y1 = sol
    for v, view in views.items():
        if not checkView(s1, view, v[0]):
            print(f"Checking {v} failed")

    s1, y1 = sol
    print(s1)
    print(y1.sum(axis=0))
    return sol

def main():
    tstart = time.time()
    s1, _ = findSolution(data.vals_list_1, data.views_1, find_all_solutions=False)
    s2, _ = findSolution(data.vals_list_2, data.views_2, find_all_solutions=False)
    s3, _ = findSolution(data.vals_list_3, data.views_3, find_all_solutions=False)
    s4, _ = findSolution(data.vals_list_4, data.views_4, find_all_solutions=False)
    print(f'Total time: {(time.time() - tstart)*1000: .2f}ms')

    sum_of_grids = s1 + s2 + s3 + s4
    final_sol = (sum_of_grids**2).sum()
    print('=======solution grids (top-left)======')
    print(s1)
    print('=======solution grids (top-right)======')
    print(s2)
    print('=======solution grids (bot-left)======')
    print(s3)
    print('=======solution grids (bot-right)======')
    print(s4)
    print('=======sum of grids======')
    print(sum_of_grids)
    print('=======sum of squared values======')
    print(final_sol)


if __name__ == '__main__':
    main()

    # # drive individual instances
    # sol1 = main1(data.vals_list_1, data.views_1)
    # sol2 = main1(data.vals_list_2, data.views_2)
    # sol3 = main1(data.vals_list_3, data.views_3)
    # sol4 = main1(data.vals_list_4, data.views_4)

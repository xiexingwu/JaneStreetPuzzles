import numpy as np
import time
import logging

from BlockPartySolver import BlockPartySolver
from itertools import product

logging.basicConfig(filename='blockparty4.log', filemode='w',
    level=logging.INFO,
    format='[%(levelname)s] %(message)s')

ex_grid = np.array([
    [1,1,2,2,2],
    [3,1,1,4,2],
    [3,5,1,6,2],
    [3,7,7,6,6],
    [3,3,7,8,6],
], dtype=int)
ex_vals_list = (
    ((2,2), 4),
    ((1,4), 2),
    ((3,0), 3)
)
ex_vals = np.array([
    5,2,1,3,4,
    2,3,1,1,2,
    1,1,4,2,5,
    3,1,2,1,3,
    4,5,3,1,4
], dtype=int).reshape((5,5))

grid = np.array([
     1, 2, 2, 2, 3, 3, 3, 3, 3, 3,
     1, 1, 2, 2, 2, 3, 4, 4, 3, 3,
     1, 1, 5, 5, 6, 6, 7, 4, 8, 8,
     1, 1, 9, 5,10, 7, 7, 7, 8, 8,
     1, 9, 9,10,10,11,12, 7, 7, 8,
     1,13, 9,14,15,11,16,16, 8, 8,
     1,17,18,14,14,14,16,19,19,19,
    17,17,18,20,14,21,22,23,23,22,
    17,17,17,20,20,22,22,23,23,22,
    17,17,17,17,20,20,22,22,22,22
], dtype=int).reshape((10,10))

vals_list = (
    ((0,1), 3),
    ((0,5), 7),
    ((1,3), 4),
    ((2,8), 2),
    ((3,3), 1),
    ((4,0), 6),
    ((4,2), 1),
    ((5,7), 3),
    ((5,9), 6),
    ((6,6), 2),
    ((7,1), 2),
    ((8,6), 6),
    ((9,4), 5),
    ((9,8), 2),
)

def checkTaxicab(vals):
    N, _ = vals.shape
    Nv = vals.max()
    irange = [i for i in range(N)] # (0 to N)
    ijrange = list(product(irange, irange))

    correct = True

    for i,j in ijrange:
        ij2 = [(i2,j2) for i2, j2 in ijrange if vals[i2, j2] == vals[i,j] and (i2,j2) != (i,j)]
        dist = list(map(lambda ij2: BlockPartySolver.taxicabDist((i,j), ij2), ij2))
        if min(dist) < vals[i,j]:
            print(f"{vals[i,j]} at {i},{j} has a closer neighbour")
            correct = False
        if vals[i,j] not in dist:
            print(f"{vals[i,j]} at {i},{j} has no correct neighbour")
            correct = False

    return correct

def computeSol(vals):
    products = [np.product(row) for row in vals]
    return sum(products)

def findSolution(grid, vals_list, find_all_solutions = False):
    N, _ = grid.shape
    solutions = []

    tstart = time.time()
    solver = BlockPartySolver(vals_list, grid, find_all_solutions)

    for vals, _ in solver.solutions:
        solutions.append(vals)
        if not find_all_solutions:
            return solutions

    logging.debug(f'{(time.time() - tstart)*1000:.2f}ms elapsed, found {len(solutions)} solutions')

    return solutions

def main(grid, vals_list):
    tstart = time.time()
    solutions = findSolution(grid, vals_list)
    print(f'Total time: {(time.time() - tstart)*1000: .2f}ms')

    if not solutions:
        print('NO SOLUTION FOUND')
        return

    if len(solutions) > 1:
        print(f'====={len(solutions)} valid solutions found. Only showing first one.======')
    vals = solutions.pop()

    checkTaxicab(vals)

    print('-----Solution-----')
    print('---vals---')
    print(vals)
    sum_of_products = computeSol(vals)
    print(f'sum of products {sum_of_products}')

    return vals

if __name__ == '__main__':
    ex_V = main(ex_grid, ex_vals_list)
    V = main(grid, vals_list)

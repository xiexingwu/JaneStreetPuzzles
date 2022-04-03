import numpy as np
import time
import logging

from collections import Counter
from KnightsMoveSolver import KnightsMoveSolver

logging.basicConfig(filename='knights4.log', filemode='w',
    level=logging.INFO,
    format='[%(levelname)s] %(message)s')

grid = np.array([
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [ 1, 1, 1, 2, 1, 1, 1, 1, 3, 1],
    [ 1, 1, 1, 2, 1, 1, 1, 1, 3, 1],
    [ 1, 1, 2, 2, 2, 2, 4, 3, 3, 3],
    [ 5, 1, 2, 1, 1, 6, 4, 4, 4, 4],
    [ 5, 1, 1, 1, 6, 6, 6, 7, 7, 4],
    [ 5, 8, 8, 9, 6,10,10, 7, 7,11],
    [ 5,12, 8, 9, 9,13,13,13, 7,11],
    [ 5,12,14, 9,15,15,15,16,16,11],
    [12,12,14,17,17,17,17,17,16,11]
], dtype=int)
vals_list = (
    ((0,0), 12),
    ((1,6),  5),
    ((1,8), 23),
    ((2,6),  8),
    ((3,3), 14),
    ((5,1),  2),
    ((6,4), 20),
    ((7,4), 33),
    ((9,9), 28)
)

def allValidGridSums(grid, vals_list, N):
    ngrids = grid.max()
    min_n = max(vals_list, key=lambda v: v[1])[1]
    # find max grid_sum
    grid_sizes = Counter(grid.flat)
    grid_min = min(grid_sizes, key=lambda k: grid_sizes[k])
    max_grid_sum = sum(N**2 - i for i in range(grid_sizes[grid_min]))

    grid_sums = []
    for k in range(min_n//ngrids, N**2//ngrids+1):
        n = k*ngrids
        nm1 = n-1
        np1 = n+1

        if n*nm1//(2*ngrids) > max_grid_sum:
            break
        if n > min_n:
            grid_sums.append(n*nm1//(2*ngrids))
        if np1 > min_n:
            grid_sums.append(n*np1//(2*ngrids))

    return grid_sums
    # print("Hard-coded allValidGridSums")
    # return [15] if N == 5 else [75]

def computeSol(vals):
    max_squares = [row.max()**2 for row in vals]
    return sum(max_squares), max_squares

def findSolution(grid, vals_list, find_all_solutions = False):
    N, _ = grid.shape
    solutions = []

    for i, gridsum_target in enumerate(allValidGridSums(grid, vals_list, N)):
        tstart = time.time()
        NPSolver = KnightsMoveSolver(vals_list, grid, gridsum_target, find_all_solutions)

        for vals, _ in NPSolver.solutions:
            solutions.append(vals)
            if not find_all_solutions:
                return solutions

        logging.debug(f'Testing gridsum {i}={gridsum_target}: {(time.time() - tstart)*1000:.2f}ms elapsed, found {len(solutions)} solutions')

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
    print('-----Solution-----')
    print('---vals---')
    print(vals)
    max_squares_sum, max_squares = computeSol(vals)
    print(f'Squares of row-maxes {max_squares}')
    print(f'sum: {max_squares_sum}')


if __name__ == '__main__':
    main(np.array(grid, dtype=int), vals_list)
    # from tests import ex_grid, ex_vals_list
    # main(ex_grid, ex_vals_list)
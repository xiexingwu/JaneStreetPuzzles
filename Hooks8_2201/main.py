import numpy as np
from scipy.ndimage import label
import time
import logging

from NumberPlacementSolver import NumberPlacementSolver

logging.basicConfig(filename='hooks8.log', filemode='w',
    level=logging.INFO,
    format='[%(levelname)s] %(message)s')

vals_list = [
    ((0,2), 8)
]
grid = [
    [1, 2, 2, 2, 3, 4, 4, 5, 5],
    [1, 2, 6, 6, 3, 7, 4, 5, 8],
    [1, 9, 9, 6, 6, 7, 7, 8, 8],
    [1, 9,10,10, 6, 7,11,12,12],
    [1,10,10,13,13,13,11,14,14],
    [1,15,10,10,10,13,11,11,14],
    [1,15,15,16,17,13,18,18,19],
    [1, 1,16,16,17,13,18,18,19],
    [1,16,16,17,17,13,13,19,19]
]

def computeSol(vals):
    '''
    invert zeros and nonzeros, then find the connected components and get their area
    '''
    N = vals.max()
    zeros = vals.copy()
    zeros[zeros==0] = N+1
    for i in range(N):
        zeros[zeros==i+1] = 0
    labels, ncomps = label(zeros)
    sizes = [(labels==i+1).sum() for i in range(ncomps)]
    return np.prod(sizes), (labels, sizes)

def allValidHooks(hook, n):
    if n == 0:
        yield hook
        return
    for hookn in validHooks(hook, n):
        yield from allValidHooks(hookn, n-1)

def validHooks(hook, n):
    if n == 1:
        new = hook.copy()
        new[new==0] = 1
        yield new
        return

    N, _ = hook.shape
    new = 0*hook
    
    for r in range(N-n+1):
        rows = range(r,r+n)
        for c in range(N-n+1):
            cols = range(c, c+n)

            left = (rows, c)
            right = (rows, c+n-1)
            up = (r, cols)
            down = (r+n-1, cols)
            # corner in top-left
            if sum(hook[left] + hook[up]) == 0:
                new[left] = new[up] = n
                yield hook+new
                new[left] = new[up] = 0

            # corner in bot-left
            if sum(hook[left] + hook[down]) == 0:
                new[left] = new[down] = n
                yield hook+new
                new[left] = new[down] = 0
    
            # corner in top-right
            if sum(hook[right] + hook[up]) == 0:
                new[right] = new[up] = n
                yield hook+new
                new[right] = new[up] = 0

            # corner in bot-right
            if sum(hook[right] + hook[down]) == 0:
                new[right] = new[down] = n
                yield hook+new
                new[right] = new[down] = 0




def main(grid, vals_list):
    tstart = time.time()
    solution = NPSolver = NumberPlacementSolver(vals_list, grid, find_all_solutions=False)
    print(f'Total time: {(time.time() - tstart)*1000: .2f}ms')

    if not solution:
        print('NO SOLUTION FOUND')
        return

    if len(solution) > 1:
        print(f'====={len(solution)} valid solutions found. Only showing first one.======')
    hook, vals = solution[0][:2]
    print('-----Solution-----')
    print('---hook---')
    print(hook)
    print('---vals---')
    print(vals)
    area, (_, sizes) = computeSol(vals)
    print(f'Areas of {sizes}')
    print(f'Product: {area}')

    return solution[0]

if __name__ == '__main__':
    solution = main(np.array(grid, dtype=int), vals_list)
    # from tests import ex_grid, ex_vals_list
    # H, V, X, DX, RX, DH, RH, M = main(ex_grid, ex_vals_list)

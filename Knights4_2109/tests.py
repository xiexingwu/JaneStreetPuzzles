
from zmq import MAX_SOCKETS
import main

import numpy as np
import matplotlib.pyplot as plt

import unittest

ex_N = 5
ex_vals_list = [
    ((0,0),1),
    ((1,4),4),
    ((4,1),6)
]

ex_grid = np.array([
    [1,1,1,1,1],
    [1,1,1,1,1],
    [1,2,1,1,1],
    [2,2,2,2,1],
    [2,3,3,1,1]
], dtype=int)

ex_vals = np.array([
    [1,0,3,0,0],
    [0,0,0,0,4],
    [0,2,7,0,0],
    [8,0,0,5,0],
    [0,6,9,0,0]
], dtype=int)

class TestSetup(unittest.TestCase):

    def testComputeSol(self):
        sol, _ = main.computeSol(ex_vals)
        self.assertEqual(219, sol)

    def testFindSolution(self):
        solutions = main.findSolution(ex_grid, ex_vals_list)
        self.assertEqual(len(solutions), 1)

        vals = solutions.pop()
        self.assertTrue((vals == ex_vals).all())

        max_squares_sum, _ = main.computeSol(vals)
        self.assertEqual(max_squares_sum, 219)

def checkGrid(grid=main.grid):
        fig, ax = plt.subplots()
        cmap = 'tab20'
        im = ax.imshow(grid, cmap=cmap)
        plt.show()
    

if __name__ == '__main__':
    print('Check grid?[y,N]:',end='')
    if input().lower() == 'y':
        checkGrid()

    unittest.main()




import main

import numpy as np
import matplotlib.pyplot as plt

import unittest

ex_N = 5
ex_vals_list = [
    ((0,1),4),
    ((0,4),3),
    ((4,0),5),
    ((4,3),5)
]

ex_grid = np.array([
    [1,1,1,2,2],
    [3,3,1,2,4],
    [3,4,4,4,4],
    [3,5,5,5,4],
    [3,5,4,4,4]
], dtype=int)

ex_hook = np.array([
    [5,3,3,3,4],
    [5,1,2,3,4],
    [5,2,2,3,4],
    [5,4,4,4,4],
    [5,5,5,5,5]
], dtype=int)

ex_vals = np.array([
    [5,4,0,4,3],
    [0,1,2,4,0],
    [5,2,0,4,0],
    [0,3,0,3,0],
    [5,5,0,5,0]
], dtype=int)

ex_wrong_hook = np.array([
    [5,3,3,3,4],
    [5,2,2,3,4],
    [5,2,1,3,4],
    [5,4,4,4,4],
    [5,5,5,5,5]
], dtype=int)

class TestSetup(unittest.TestCase):

    def testComputeSol(self):
        sol, _ = main.computeSol(ex_vals)
        self.assertEqual(12, sol)

    def testAllValidHooks(self):
        hook = np.zeros((ex_N, ex_N), dtype=int)
        arr1 = np.array([[4, 4, 4, 4, 5],
                         [2, 2, 3, 4, 5],
                         [2, 1, 3, 4, 5],
                         [3, 3, 3, 4, 5],
                         [5, 5, 5, 5, 5]], dtype=int)
        arr2 = np.array([[5, 4, 4, 4, 4],
                         [5, 4, 3, 3, 3],
                         [5, 4, 2, 1, 3],
                         [5, 4, 2, 2, 3],
                         [5, 5, 5, 5, 5]], dtype=int)
        arr1_found = False
        arr2_found = False
        ex_found = False

        count = 0
        expected_count = 4**(ex_N-1)
        for new_hook in main.allValidHooks(hook, ex_N):
            count += 1
            if (new_hook == arr1).all():
                arr1_found = True
            elif (new_hook == arr2).all():
                arr2_found = True
            elif (new_hook == ex_hook).all():
                ex_found = True

        self.assertEqual(count, expected_count) # should be 4^(N-1) total configs
        self.assertTrue(arr1_found and arr2_found and ex_found)

    def testFindSolution(self):
        solutions = main.findSolution(ex_grid, ex_vals_list)
        self.assertEqual(len(solutions), 1)

        hook, vals = solutions.pop()
        self.assertTrue((hook == ex_hook).all())
        self.assertTrue((vals == ex_vals).all())

        area, _ = main.computeSol(vals)
        self.assertEqual(area, 12)
        
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



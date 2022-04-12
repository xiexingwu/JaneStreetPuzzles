# Files

* `twentyfourseven2.pdf`

    Problem description taken from the Jane Street puzzle archive (December 2020).

* `main.py`

    Main script to run to solve the problem - takes about < 1 sec on M1 Pro. 

    Solution:
    ```
    Total time:  431.56ms
    =======solution grids (top-left)======
    [[5 4 4 0 0 7 0]
     [0 0 7 6 3 4 0]
     [5 6 2 0 7 0 0]
     [0 3 0 0 6 6 5]
     [5 7 0 6 0 0 2]
     [5 0 7 1 0 0 7]
     [0 0 0 7 4 3 6]]
    =======solution grids (top-right)======
    [[7 2 5 6 0 0 0]
     [2 0 0 5 7 6 0]
     [5 7 4 0 0 4 0]
     [0 0 6 0 4 3 7]
     [6 4 0 0 3 0 7]
     [0 7 5 3 0 0 5]
     [0 0 0 6 6 7 1]]
    =======solution grids (bot-left)======
    [[7 2 0 0 4 7 0]
     [0 6 7 5 2 0 0]
     [4 5 0 5 0 0 6]
     [0 0 0 7 7 1 5]
     [6 7 3 0 0 0 4]
     [3 0 6 0 0 6 5]
     [0 0 4 3 7 6 0]]
    =======solution grids (bot-right)======
    [[0 0 0 1 5 7 7]
     [0 2 5 7 0 0 6]
     [3 7 0 7 0 0 3]
     [4 0 0 0 5 7 4]
     [0 5 6 5 4 0 0]
     [6 0 6 0 6 2 0]
     [7 6 3 0 0 4 0]]
    =======sum of grids======
    [[19  8  9  7  9 21  7]
     [ 2  8 19 23 12 10  6]
     [17 25  6 12  7  4  9]
     [ 4  3  6  7 22 17 21]
     [17 23  9 11  7  0 13]
     [14  7 24  4  6  8 17]
     [ 7  6  7 16 17 20  7]]
    =======sum of squared values======
    8520
    ```

* `TwentyFourSevenSolver.py`
    
    The class used to solve the integer programming problem for a particular instance.

* `main_cpsat.ipynb`

    Documents the mathematical theory behind 
    some of the constraints and how they are implemented using the CP-SAT 
    solver in Google's `ortools` module.
    
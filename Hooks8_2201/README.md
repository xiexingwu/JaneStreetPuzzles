# Files

* `hooks8.pdf`

    Problem description taken from the Jane Street puzzle archive (January 2022).

* `main.py`

    Main script to run to solve the 9x9 problem - takes 10-15 mins on M1 Pro. 

    Solution:
    ```
    ---hook---
    [[9 8 7 6 6 6 6 6 6]
     [9 8 7 5 5 5 5 5 6]
     [9 8 7 3 3 3 4 5 6]
     [9 8 7 3 2 2 4 5 6]
     [9 8 7 3 2 1 4 5 6]
     [9 8 7 4 4 4 4 5 6]
     [9 8 7 7 7 7 7 7 7]
     [9 8 8 8 8 8 8 8 8]
     [9 9 9 9 9 9 9 9 9]]
    ---vals---
    [[5 7 8 0 6 0 6 0 6]
     [5 0 0 9 9 9 9 9 6]
     [5 7 8 4 0 4 0 9 0]
     [0 0 0 4 2 2 3 9 6]
     [0 0 8 4 0 1 0 9 0]
     [0 0 0 3 0 0 3 9 6]
     [0 7 8 8 8 0 8 0 8]
     [0 0 7 0 7 0 7 0 7]
     [0 0 0 0 0 5 5 0 0]]
    Areas of [1, 1, 1, 2, 1, 1, 1, 17, 5, 1, 1, 4]
    Product: 680
    ```
    
    Method overview:
    
    * Generate all configurations of hooks
    * For each hook configuration, solve the integer programming problem of 
    placing numbers in the hooks (only constraint not implemented is 
    the connectedness of values).
    * If there are candidate solutions, they are then checked against the 
    connectedness constraint.

* `NumberPlacementSolver.py`
    
    The class used to solve the integer programming problem for a given hook 
    configuration.
    
* `main_cpsat.ipynb`

    Obsolete in terms of code, but documents the mathematical theory behind 
    some of the constraints and how they are implemented using the CP-SAT 
    solver in Google's `ortools` module.
    
    
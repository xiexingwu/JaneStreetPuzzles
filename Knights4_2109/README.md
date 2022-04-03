# Files

* `knights4.pdf`

    Problem description taken from the Jane Street puzzle archive (September 2021).

* `main.py`

    Main script to run to solve the 10x10 problem - takes about 1 minute on M1 Pro. 

    Solution:
    ```
    ---vals---
    [[12  0  0  0  0  9  0  7  0  0]
     [ 0  0 13 10  0  0  5  0 23  0]
     [ 0 11  0 17  4  0  8  0  6  0]
     [ 1  0  0 14  0 18  0 22  0 24]
     [ 0  0 16  3  0 21 50 25  0  0]
     [ 0  2  0  0 15  0 19 48  0  0]
     [ 0 41 34  0 20 49 26  0  0 47]
     [35 38  0 42 33 30 45  0 27  0]
     [40  0 36  0  0 43 32 29 46  0]
     [37  0 39  0 31  0  0 44  0 28]]
    Squares of row-maxes [144, 529, 289, 576, 2500, 2304, 2401, 2025, 2116, 1936]
    sum: 14820
    ```
    
    Method overview:
    
    * Generate all possible grid sums.
    * For each grid sum, solve the integer programming problem of taking knight moves until the grid sum is satisfied.
        * Currently, code implements if $v$ exists, then $v-1$ must also exist. If we instead require $N$ total steps taken (which is the same as specifying the grid sum), then setting the domain of $v$ to exactly $[0, N]$ may improve solution speed.

* `KnightsMoveSolver.py`
    
    The class used to solve the integer programming problem for a given grid sum.
    
* `main_cpsat.ipynb`

    Obsolete in terms of code, but documents the mathematical theory behind 
    some of the constraints and how they are implemented using the CP-SAT 
    solver in Google's `ortools` module.
    
    
# Files

* `AlmostMagic.pdf`

    Problem description taken from the Jane Street puzzle archive (April 2022).

* `main.py`

    Main script to run to solve the problem - takes about 5 minutes on M1 Pro. 

    Solution:
    ```
    ---------Solution----------
    sol = [26, 2, 34, 29, 21, 13, 4, 18, 24, 7, 39, 16, 12, 6, 37, 23, 9, 5, 19, 10, 8, 40, 22, 11, 1, 3, 17, 14]
    sum of values = 470
    -------------------
    |  |26| 2|34|  |  |
    -------------------
    |  |29|21|13| 4|18|
    -------------------
    |24| 7|39|16|12| 6|
    -------------------
    |37|23| 9| 5|19|10|
    -------------------
    | 8|40|22|11| 1|  |
    -------------------
    |  |  | 3|17|14|  |
    -------------------
    ```
    
    Method overview:
    
    * Mixed integer programming (MIP):
        * constrain sums in each square
        * constrain uniqueness (tricky, uses big M notation)
        * minimize sum of all values
    
* `main_mip.ipynb`

    Documents the mathematical theory behind the MIP model,
    the constraints, and how they are implemented using the `pywraplp`  
    solver in Google's `ortools.linear_solver` module.
    
* `main_cpsat.ipynb`
    
    As above, but using the CP-SAT solver, i.e. constraint programming.
    
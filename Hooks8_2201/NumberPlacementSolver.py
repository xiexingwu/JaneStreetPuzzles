from ortools.sat.python import cp_model

import numpy as np
from itertools import product

import logging

class NumberPlacementSolver(cp_model.CpSolverSolutionCallback):
    '''
    Solves placement of numbers for some hook configuration
    '''
    def __init__(self, 
                vals_list: tuple[tuple[int, int], int], 
                grid: np.ndarray,
                hook: np.ndarray,
                find_all_solutions: bool):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.find_all_solutions = find_all_solutions
        self.solutions = []
        status = self.solveNumberPlacement(vals_list, grid, hook)

        if status == cp_model.INFEASIBLE:
            # print('No solution found')
            pass
        elif status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
            logging.info(f'{len(self.solutions)} potential configurations found')

    def on_solution_callback(self):
        solution = self.assignSol()
        self.solutions.append(solution)

    def assignSol(self):
        N = self.N
        x = self.x
        m = self.m
        X = np.zeros((N, N, N+1), dtype=int)
        M = np.zeros((N, N+1), dtype=int)
        V = np.zeros((N, N), dtype=int)
        Nrange = [i+1 for i in range(N)] # (1 to N)
        for r, c in product(Nrange, Nrange):
            for v in range(N+1):
                if self.Value(x[r,c,v]):
                    X[r-1,c-1,v] = 1
                    V[r-1,c-1] += v
        for h,v in product(Nrange, range(N+1)):
            if self.Value(m[h,v]):
                M[h-1,v] = 1
        return V, M, X

    def solveNumberPlacement(self, vals_list, grid, hook):
        model = cp_model.CpModel()

        N, _ = grid.shape
        self.N = N # store N for convenience

        ngrids = grid.max()
        gridsum_target = N*(N+1)*(2*N+1)//(6*ngrids)

        Nrange = [i+1 for i in range(N)] # (1 to N)
        Vrange = [i for i in range(N+1)] # value (0 to N)
        Grange = [i+1 for i in range(ngrids)] # grid index
        RC   = list(product(*[Nrange]*2))

        ## Define and save variables
        x = {}
        for r,c in RC:
            for v in Vrange:
                x[r,c,v] = model.NewBoolVar(f'x[{r},{c},{v}]')
        m = {}
        for h,v in product(Nrange, Vrange):
            m[h,v] = model.NewBoolVar(f'm[{h},{v}]')

        self.x = x
        self.m = m

        ## UNIQUENESS constraints
        # each (r,c) has one unique v
        for r,c in RC:
            model.AddExactlyOne(x[r,c,v] for v in Vrange)
        # each (h) maps to 1 positive (v)
        for v in Vrange:
            if v > 0:
                model.AddExactlyOne(m[h,v] for h in Nrange)
        for h in Nrange:
                model.AddExactlyOne(m[h,v] for v in Vrange if v > 0)
                model.Add(m[h,0] == 0)

        ## SPARSITY constraint (one zero in every 2x2 submatrix)
        for r,c in RC:
            if r < N and c < N:
                mat22 = (x[r  ,c,v] + x[r  ,c+1,v] +
                        x[r+1,c,v] + x[r+1,c+1,v]
                        for v in Vrange if v > 0)
                model.Add(sum(mat22) <= 3)

        # Value
        for h in Nrange:
            for v in Vrange:
                if v > 0:
                    model.Add(sum(x[r,c,v] for r,c in RC if hook[r-1,c-1] == h) == v*m[h,v])

        # prescribed values
        for (i,j), val in vals_list:
            model.Add(x[i+1,j+1,val] == 1)
        # correct grid sum
        for g in Grange:
            subgrid_sum = sum(v*x[r,c,v] for r,c in RC for v in Vrange if grid[r-1,c-1] == g)
            model.Add(subgrid_sum == gridsum_target)

        # SOLVE
        solver = cp_model.CpSolver()
        solver.parameters.enumerate_all_solutions = self.find_all_solutions
        status = solver.Solve(model, self)
        return status

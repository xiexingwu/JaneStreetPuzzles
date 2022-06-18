from ortools.sat.python import cp_model

import numpy as np
from itertools import product

import logging

class BlockPartySolver(cp_model.CpSolverSolutionCallback):
    def __init__(self, 
                vals_list: tuple[tuple[int, int], int], 
                grid: np.ndarray,
                find_all_solutions: bool):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.find_all_solutions = find_all_solutions
        self.solutions = []
        status = self.solveBlockParty(vals_list, grid)

        if status == cp_model.INFEASIBLE:
            pass
        elif status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
            logging.info(f'{len(self.solutions)} potential configurations found')

    def on_solution_callback(self):
        solution = self.assignSol()
        self.solutions.append(solution)

    def assignSol(self):
        N = self.N
        Nv = self.Nv
        x = self.x
        X = np.zeros((N, N, Nv), dtype=int)
        V = np.zeros((N, N), dtype=int)
        irange = [i for i in range(N)] # (0 to N)
        ijrange = list(product(irange, irange))
        vrange = [v for v in range(1, Nv+1)] # (1 to M)
        for i,j in ijrange:
            for v in vrange:
                if self.Value(x[i,j,v]):
                    X[i,j,v-1] = 1
                    V[i,j] += v
        return V, X

    @staticmethod
    def taxicabDist(ij1: tuple[int, int], ij2: tuple[int, int]) -> int:
        '''
        Taxicab distance between (i1,j1) and (i2,j2) minus v
        '''
        i1, j1 = ij1
        i2, j2 = ij2
        di = abs(i2-i1)
        dj = abs(j2-j1)
        return di + dj

    def solveBlockParty(self, vals_list, grid):
        model = cp_model.CpModel()

        N, _ = grid.shape
        self.N = N

        ngrids = grid.max()

        Nv = max((grid==g).sum() for g in range(1, ngrids+1)) # maximum number
        self.Nv = Nv

        irange = [n for n in range(N)] # (0 to N-1)
        ijrange = list(product(irange, irange))
        vrange = [v for v in range(1, Nv+1)] # (1 to M)
        Grange = [g+1 for g in range(ngrids)] # grid index

        ## Define and save variables
        x = {}
        for i,j in ijrange:
            for v in vrange:
                x[i,j,v] = model.NewBoolVar(f'x[{i},{j},{v}]')
        self.x = x


        ## UNIQUENESS constraints
        # each (i,j) has exactly one (v)
        for i,j in ijrange:
            model.AddExactlyOne(x[i,j,v] for v in vrange)

        ## Taxicab constraint
        M = Nv+1 # big M - 
        for i,j in ijrange:
            for v in vrange:
                ij_taxi_edge = [(i2,j2) for i2,j2 in ijrange if self.taxicabDist((i,j), (i2,j2)) == v]
                model.Add(sum(x[i,j,v] for i,j in ij_taxi_edge) >= x[i,j,v])

                ij_taxi_inner = [(i2,j2) for i2,j2 in ijrange if self.taxicabDist((i,j), (i2,j2)) < v]
                model.Add(sum(x[i,j,v] for i,j in ij_taxi_inner) <= M*(1-x[i,j,v]) +1) # +1 for self

        # prescribed values
        for (i,j), val in vals_list:
            model.Add(x[i,j,val] == 1)
        # 1 to Ng appears in each grid of size Ng
        for g in Grange:
            Mg = (grid==g).sum()
            ij_grid = [(i,j) for i,j in ijrange if grid[i,j] == g]
            for v in range(1, Mg+1):
                model.AddExactlyOne(x[i,j,v] for i,j in ij_grid)

        # SOLVE
        solver = cp_model.CpSolver()
        solver.parameters.enumerate_all_solutions = self.find_all_solutions
        status = solver.Solve(model, self)
        return status


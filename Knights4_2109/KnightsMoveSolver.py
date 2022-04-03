from ortools.sat.python import cp_model

import numpy as np
from itertools import product

import logging

class KnightsMoveSolver(cp_model.CpSolverSolutionCallback):
    def __init__(self, 
                vals_list: tuple[tuple[int, int], int], 
                grid: np.ndarray,
                gridsum_target: int,
                find_all_solutions: bool):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.find_all_solutions = find_all_solutions
        self.solutions = []
        status = self.solveKnightsMove(vals_list, grid, gridsum_target)

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
        X = np.zeros((N**2, N**2+1), dtype=int)
        V = np.zeros((N, N), dtype=int)
        nrange = [i for i in range(N**2)] # (0 to N^2)
        vrange = [i for i in range(N**2+1)] # (0 to N^2)
        for n in nrange:
            for v in vrange:
                if self.Value(x[n,v]):
                    X[n,v] = 1
                    V[self.n2ij(n)] += v
        return V, X

    def n2ij(self, n):
        i = n // self.N
        j = n - i*self.N
        return (i,j)
    def ij2n(self, i,j):
        return i*self.N + j

    def isKnightsMove(self, n1, n2):
        '''
        True if n1 and n2 are knights move away
        '''
        i1, j1 = self.n2ij(n1)
        i2, j2 = self.n2ij(n2)
        di = abs(i2-i1)
        dj = abs(j2-j1)
        if (di == 2 and dj == 1) or (di == 1 and dj == 2):
            return 1
        else:
            return 0

    def solveKnightsMove(self, vals_list, grid, gridsum_target):
        model = cp_model.CpModel()

        N, _ = grid.shape
        self.N = N

        ngrids = grid.max()

        nrange = [n for n in range(N**2)] # (0 to N^2-1)
        vrange = [v for v in range(N**2+1)] # (0 to N^2)
        Grange = [g+1 for g in range(ngrids)] # grid index

        e = [[self.isKnightsMove(n1,n2) if n1 != n2 else 0 for n1 in nrange] for n2 in nrange]

        ## Define and save variables
        x = {}
        for n in nrange:
            for v in vrange:
                x[n,v] = model.NewBoolVar(f'x[{n},{v}]')
        self.x = x


        ## UNIQUENESS constraints
        # each (n) has exactly one (v) (including 0)
        for n in nrange:
            model.AddExactlyOne(x[n,v] for v in vrange)
        # each (v>0) allocated at exactly one (n)
        for v in vrange:
            if v > 0:
                model.AddAtMostOne(x[n,v] for n in nrange)

        ## Knight's move constraint
        for n in nrange:
            for v in vrange:
                if v >= 1 and v <= N**2-1:
                    nn = [i for i in nrange if i != n and not e[i][n]]
                    model.Add(sum(x[i,v+1] for i in nn) <= 1 - x[n,v])
                if v >= 2 and v <= N**2:
                    model.Add(sum(x[i, v-1] for i in nrange) >= x[n,v])

        # prescribed values
        for (i,j), val in vals_list:
            model.Add(x[self.ij2n(i,j),val] == 1)
        # correct grid sum
        for g in Grange:
            subgrid_sum = sum(v*x[n,v] for n in nrange for v in vrange if grid[self.n2ij(n)] == g)
            model.Add(subgrid_sum == gridsum_target)

        # SOLVE
        solver = cp_model.CpSolver()
        solver.parameters.enumerate_all_solutions = self.find_all_solutions
        status = solver.Solve(model, self)
        return status


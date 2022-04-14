from ortools.sat.python import cp_model
from scipy.ndimage import label
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
                find_all_solutions: bool = False):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.find_all_solutions = find_all_solutions
        self.solutions = []
        status = self.solveNumberPlacement(vals_list, grid)

        if status == cp_model.INFEASIBLE:
            # print('No solution found')
            pass
        elif status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
            logging.info(f'{len(self.solutions)} potential configurations found')

    def on_solution_callback(self):
        solution = self.assignSol()
        if self.checkConnected(solution[1]):
            self.solutions.append(solution)
            logging.info(f'Found a potential solution.')
            if not self.find_all_solutions:
                logging.info(f'Manully stopping search.')
                self.StopSearch()

    def checkConnected(vals):
        _, ncomps = label(vals)
        return ncomps==1

    def assignSol(self):
        N = self.N
        x = self.x
        m = self.m
        dh = self.dh
        rh = self.rh
        X = np.zeros((N, N, N+1, N+1), dtype=int)
        M = np.zeros((N, N+1), dtype=int)
        H = np.zeros((N, N), dtype=int)
        V = np.zeros((N, N), dtype=int)
        DH = np.zeros((N, N), dtype=int)
        RH = np.zeros((N, N), dtype=int)
        Nrange = [i+1 for i in range(N)] # (1 to N)
        for i,j in product(Nrange, Nrange):
            for h in Nrange:
                for v in range(N+1):
                    if self.Value(x[i,j,h,v]):
                        X[i-1,j-1,h,v] = 1
                        V[i-1,j-1] += v
                        H[i-1,j-1] += h
                    if i < N and self.Value(dh[i,j,h]):
                        DH[i-1,j-1] += 1
                    if j < N and self.Value(rh[i,j,h]):
                        RH[i-1,j-1] += 1
        for h in Nrange:
            for v in range(N+1):
                if self.Value(m[h,v]):
                    M[h-1,v] = 1
        return (H, V, X, 
            DH, RH, M)

    def solveNumberPlacement(self, vals_list, grid):
        model = cp_model.CpModel()

        N, _ = grid.shape
        self.N = N # store N for convenience

        ngrids = grid.max()
        gridsum_target = N*(N+1)*(2*N+1)//(6*ngrids)

        Nrange = [i+1 for i in range(N)] # (1 to N)
        Vrange = [i for i in range(N+1)] # value (0 to N)
        Grange = [i+1 for i in range(ngrids)] # grid index
        ijrange   = list(product(*[Nrange]*2))

        ## Define and save variables
        #------------ x --------------
        x = {}
        for i,j in ijrange:
            for h in Nrange:
                for v in Vrange:
                    x[i,j,h,v] = model.NewBoolVar(f'x[{i},{j},{h},{v}]')

        # each (r,c) has one unique v
        for i,j in ijrange:
            model.AddExactlyOne(x[i,j,h,v] for h in Nrange for v in Vrange)
        
        # SPARSITY constraint (one zero in every 2x2 submatrix)
        for i,j in ijrange:
            if i < N and j < N:
                mat22 = (x[i  ,j,h,v] + x[i  ,j+1,h,v] +
                         x[i+1,j,h,v] + x[i+1,j+1,h,v]
                        for h in Nrange
                        for v in Vrange if v > 0)
                model.Add(sum(mat22) <= 3)

        # each hook has size 2h-1
        for h in Nrange: 
            model.Add(sum(x[i,j,h,v] for i,j in ijrange for v in Vrange) == 2*h-1)


        #------------ z: Location of hooks --------------
        z = {}
        for i,j in ijrange:
            for h in Nrange:
                z[i,j,h] = model.NewBoolVar(f'z[{i},{j},{h}]')
        # each hook has one associated (row, col)
        for h in Nrange: 
            model.AddExactlyOne(z[i,j,h] for i,j in ijrange)

        #------------ dh, rh: Adjacency of hooks --------------
        dh = {}
        rh = {}
        for h in Nrange:
            for i,j in ijrange:
                if i < N:
                    dh[i,j,h] = model.NewBoolVar(f'd[{i},{j},{h}]')
                    model.Add(2*dh[i,j,h] <= sum(x[i,j,h,v] + x[i+1,j,h,v] for v in Vrange))
                if j < N:
                    rh[i,j,h] = model.NewBoolVar(f'r[{i},{j},{h}]')
                    model.Add(2*rh[i,j,h] <= sum(x[i,j,h,v] + x[i,j+1,h,v] for v in Vrange))
            # adjacency of hooks is h-1 in each direction
            model.Add(sum(dh[i,j,h] for i,j in ijrange if i < N) == h-1)
            model.Add(sum(rh[i,j,h] for i,j in ijrange if j < N) == h-1)

        # constrain adjacencies to exist on same row/col
        for h in Nrange:
            if h == 1: 
                continue
            for j in Nrange:
                model.Add(sum(dh[i,j,h] for i in Nrange if i < N) <= (h-1) * sum(z[i,j,h] for i in Nrange))
            for i in Nrange:
                model.Add(sum(rh[i,j,h] for j in Nrange if j < N) <= (h-1) * sum(z[i,j,h] for j in Nrange))

        #------------ m: Association of h with v --------------
        m = {}
        for h,v in product(Nrange, Vrange):
            m[h,v] = model.NewBoolVar(f'm[{h},{v}]')

        # each (h) maps to 1 positive (v)
        for v in Vrange:
            if v > 0:
                model.AddExactlyOne(m[h,v] for h in Nrange)
        for h in Nrange:
                model.AddExactlyOne(m[h,v] for v in Vrange if v > 0)
                model.Add(m[h,0] == 0)

        self.x = x
        self.dh = dh
        self.rh = rh
        self.z = z
        self.m = m

        # Value
        for h in Nrange:
            for v in Vrange:
                if v > 0:
                    model.Add(sum(x[i,j,h,v] for i,j in ijrange) == v*m[h,v])

        # prescribed values
        for (r,c), val in vals_list:
            model.Add(sum(x[r+1,c+1,h,val] for h in Nrange) == 1)

        # correct grid sum
        for g in Grange:
            subgrid_sum = 0
            for i,j in ijrange:
                if grid[i-1,j-1] != g:
                    continue
                subgrid_sum += sum(v*x[i,j,h,v] for h in Nrange for v in Vrange)
            model.Add(subgrid_sum == gridsum_target)

        # SOLVE
        solver = cp_model.CpSolver()
        solver.parameters.enumerate_all_solutions = True # Using check_connected, have to enumerate all 
        status = solver.Solve(model, self)
        return status

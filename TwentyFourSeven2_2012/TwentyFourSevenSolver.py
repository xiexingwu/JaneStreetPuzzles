from ortools.sat.python import cp_model
from itertools import product
import numpy as np
import logging

class TwentyFourSevenSolver(cp_model.CpSolverSolutionCallback):
    def __init__(self, 
                vals_list, 
                top_view,
                bot_view,
                lft_view,
                rgt_view,
                find_all_solutions: bool):

        self.N = 7
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.find_all_solutions = find_all_solutions
        self.solutions = []
        status = self.solveTwentyFourSeven(vals_list, top_view, bot_view, lft_view, rgt_view)

        if status == cp_model.INFEASIBLE:
            logging.info(f'NO SOLUTION FOUND')
            pass
        elif status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
            logging.info(f'{len(self.solutions)} potential configurations found')
            logging.info(self.solutions[0][0])

    def on_solution_callback(self):
        solution = self.assignSol()
        self.solutions.append(solution)

    def assignSol(self):
        N = self.N
        x = self.x
        y = self.y
        X = np.zeros((N**2, 8), dtype=int)
        V = np.zeros((N, N), dtype=int)
        Y = np.zeros((2, N, N), dtype=int)
        nrange = self.nrange
        vrange = self.vrange
        erange = self.erange
        for n in nrange:
            for v in vrange:
                if self.Value(x[n,v]):
                    X[n,v] = 1
                    V[self.n2ij(n)] += v
        for i,j in erange:
            nl = self.ij2n(i  , j  )
            nr = self.ij2n(i  , j+1)
            nu = self.ij2n(j  , i  )
            nd = self.ij2n(j+1, i  )
            if self.Value(y[nl,nr]):
                Y[0,i,j] = 1
            if self.Value(y[nu,nd]):
                Y[1,j,i] = 1
        return V, X, Y

    def n2ij(self, n, N=None):
        N = self.N if N is None else N
        i = n // N
        j = n - i*N
        return (i,j)

    def ij2n(self, i, j, N=None):
        N = self.N if N is None else N
        return i*N + j

    def solveTwentyFourSeven(self, vals_list, top_view, bot_view, lft_view, rgt_view):
        model = cp_model.CpModel()
        self.model = model

        N = self.N

        nrange = [n for n in range(N**2)] # (0 to N^2-1)
        vrange = [v for v in range(8)] # (0 to 7)
        erange = list(product(range(N), range(N-1))) # (0 to N-1) x (0 to N-2)
        self.nrange = nrange
        self.vrange = vrange
        self.erange = erange

        ## Define and save variables
        x = {}
        for n in nrange:
            for v in vrange:
                x[n,v] = model.NewBoolVar(f'x[{n},{v}]')
        self.x = x
        y = {}
        for i,j in erange: 
            nl = self.ij2n(i  , j  )
            nr = self.ij2n(i  , j+1)
            nu = self.ij2n(j  , i  )
            nd = self.ij2n(j+1, i  )
            y[nl,nr] = model.NewBoolVar(f'y[{nl},{nr}]')
            y[nu,nd] = model.NewBoolVar(f'y[{nu},{nd}]')
            # edge existence constraint
            model.Add(2*y[nl,nr] <= sum(x[nl,v] + x[nr,v] for v in vrange if v != 0))
            model.Add(2*y[nu,nd] <= sum(x[nu,v] + x[nd,v] for v in vrange if v != 0))
        self.y = y

        # each (n) has exactly one (v) (including 0)
        for n in nrange:
            model.AddExactlyOne(x[n,v] for v in vrange)

        # each (v>0) allocated (v) times
        for v in vrange:
            if v > 0:
                model.Add(sum(x[n,v] for n in nrange) == v)

        # four (v>0) per row/col, summing to 20
        for i in range(N):
            model.Add(sum(  x[self.ij2n(i,j),v] for v in vrange for j in range(N) if v > 0) == 4)
            model.Add(sum(v*x[self.ij2n(i,j),v] for v in vrange for j in range(N)) == 20)
            model.Add(sum(  x[self.ij2n(j,i),v] for v in vrange for j in range(N) if v > 0) == 4)
            model.Add(sum(v*x[self.ij2n(j,i),v] for v in vrange for j in range(N)) == 20)

        # no 2x2 filled subgrid
        for i,j in product(range(N-1), range(N-1)):
            mat22 = (x[self.ij2n(i  ,j),v] + x[self.ij2n(i  ,j+1),v] +
                     x[self.ij2n(i+1,j),v] + x[self.ij2n(i+1,j+1),v]
                     for v in vrange if v > 0)
            model.Add(sum(mat22) <= 3)

        # connected component (total edges = (nnz-1))
        nnz = sum(v for v in vrange) # number of elements = one 1, two 2, ... seven 7's, should be 28

        model.Add(
            sum(
                y[self.ij2n(i,j),self.ij2n(i, j+1)] + 
                y[self.ij2n(j,i),self.ij2n(j+1, i)]
                for i,j in erange)
            == nnz-1)

        ## top-bot-left-right views correct
        self.addViewConstraint(top_view, "t")
        self.addViewConstraint(bot_view, "b")
        self.addViewConstraint(lft_view, "l")
        self.addViewConstraint(rgt_view, "r")

        # prescribed values
        for (i,j), val in vals_list:
            model.Add(x[self.ij2n(i,j),val] == 1)

        # SOLVE
        solver = cp_model.CpSolver()
        solver.parameters.enumerate_all_solutions = self.find_all_solutions
        status = solver.Solve(model, self)
        return status

    def addViewConstraint(self, view, side):
        if not view: # i.e. empty constraint
            logging.debug("skipping constraint")
            return
        x = self.x
        N = self.N
        vrange = self.vrange

        M = 10 # penalty for if target v appeared already (6 should be sufficient)

        # left and top views just see head of row/col
        if side == "l" or side == "t":
            jprange = lambda j: range(j)
        # right and bot views just see tail of row/col
        elif side == "r" or side == "b":
            jprange = lambda j: range(j+1, N)

        # top and bottom look at columns, i.e. transposed
        if side == "t" or side == "b":
            ij2n = lambda i, j: self.ij2n(j,i)
        elif side == "l" or side == "r":
            ij2n = self.ij2n

        for it, vt in view:
            for j in range(N):
                v_before  = sum(x[ij2n(it,jp),v ] for jp in jprange(j) for v in vrange if v not in (0, vt))
                vt_before = sum(x[ij2n(it,jp),vt] for jp in jprange(j))
                self.model.Add(v_before <= M*vt_before)

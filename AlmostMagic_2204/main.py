import time

from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver('SCIP')        
x = {}
b = {}

from itertools import combinations

# indexes
#      1,  2,  3
#      4,  5,  6,  7,  8
#  9, 10, 11, 12, 13, 14
# 15, 16, 17, 18, 19, 20
# 21, 22, 23, 24, 25
#         26, 27, 28 
#
# Square 1
sq1 = [
     1, 2, 3,
     4, 5, 6,
    10,11,12]
sq2 = [
     6, 7, 8,
    12,13,14,
    18,19,20]
sq3 = [
     9,10,11,
    15,16,17,
    21,22,23]
sq4 = [
    17,18,19,
    23,24,25,
    26,27,28]
sqs = [sq1, sq2, sq3, sq4]
ex_sol = [50, 72, 16, 12, 46, 80, 75, 53, 77, 76, 20, 43, 69, 96, 1, 58, 114, 85, 64, 59, 95, 40, 39, 88, 137, 111, 90, 62]
sol = [26,  2, 34, 29, 21, 13,  4, 18, 24,  7, 39, 16, 12,  6, 37, 23,  9, 5, 19, 10,  8, 40, 22, 11,  1,  3, 17, 14]

horzs = [slice(3*i, 3*i+3  ) for i in range(3)] # horizontal
verts = [slice(  i,     9,3) for i in range(3)] # vertical
diags = [slice(  0,     9,4), # main diag
         slice(  2,     7,2)] # off diag


def checkMagic(square):
    sums = []
    sums += [sum(square[horz]) for horz in horzs]
    sums += [sum(square[vert]) for vert in verts]
    sums += [sum(square[diag]) for diag in diags]
    
    # print(f"sums: {sums}")
    if max(sums) - min(sums) > 1:
        return False
    return True


def computeSol(sol):
    squares = [[sol[i-1] for i in sq] for sq in sqs]
    # for square in squares:
    for sq in sqs:
        square = [sol[i-1] for i in sq]
        if not checkMagic(square):
            print(f"Invalid almost magic square: {sq}")
            return -1

    return sum(sol)

def findSolution():

    ## Define and save variables
    infinity = solver.infinity()
    nrange = [i+1 for i in range(28)]
    for n in nrange:
        x[n] = solver.IntVar(1., infinity, f'x[{n}]')
    for n1, n2 in combinations(nrange, 2):
            b[n1,n2] = solver.BoolVar(f'b[{n1},{n2}]')

    ## Uniqueness constraints
    M = 1828 # max M
    for n1, n2 in combinations(nrange, 2):
            solver.Add(x[n1] >= x[n2] +    b[n1,n2]  - M*(1-b[n1,n2]))
            solver.Add(x[n2] >= x[n1] + (1-b[n1,n2]) - M*   b[n1,n2] )


    ## Sums constraints
    for sq in sqs:
        sums = [sum(x[n] for n in sq[sum_slice]) for sum_slice in horzs + verts + diags]
        for sum1, sum2 in combinations(sums, 2):
            solver.Add(sum1 - sum2 <=  1)
            solver.Add(sum1 - sum2 >= -1)

    solver.Add(sum(x[n] for n in nrange) <= 1828)


    solver.Minimize(sum(x[n] for n in nrange))

    status = solver.Solve()
    return status

def assignSol():
    X = []
    for i in range(28):
        X.append(round(x[i+1].solution_value()))
    return X

def printSolutionGrid(sol):
    sol_str = [str(s) for s in sol]
    strlen = max((len(s) for s in sol_str))
    row_inds = [
            (2, [      1,  2,  3]),
            (2, [      4,  5,  6,  7,  8]),
            (1, [  9, 10, 11, 12, 13, 14]),
            (1, [ 15, 16, 17, 18, 19, 20]),
            (1, [ 21, 22, 23, 24, 25]),
            (3, [         26, 27, 28]),
        ]
    print('-'+6*('-'*strlen+'-'))
    for start, inds in row_inds:
        print('|',end='')
        for i in range(start-1):
            print(''.rjust(strlen), end='|')
        for ind in inds:
            print(sol_str[ind-1].rjust(strlen),end='|')
        for i in range(6-len(inds)-start+1):
            print(''.rjust(strlen), end='|')
        print('')
        print('-'+6*('-'*strlen+'-'))


def main():
    tstart = time.time()
    status = findSolution()
    print(f"Time taken: {(time.time() - tstart)*1000}ms")
    if status != pywraplp.Solver.OPTIMAL:
        print('The problem does not have an optimal solution.')
        return 
    
    X = assignSol()
    print('---------Solution----------')
    print(f'sol = {X}')
    print(f'sum of values = {computeSol(X)}')
    printSolutionGrid(X)

if __name__ == "__main__":
    main()
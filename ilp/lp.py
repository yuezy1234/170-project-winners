from ortools.linear_solver import pywraplp
import math

# Inputs
D = 30
N = 25
Rs = 3
Rp = 8
cities = [
    [0  , 28],
    [4  , 28],
    [2  , 27],
    [6  , 26],
    [1  , 25],
    [7  , 24],
    [9  , 23],
    [3  , 23],
    [3  , 21],
    [8  , 21],
    [6  , 19],
    [9  , 18],
    [23 , 12],
    [28 , 11],
    [22 , 10],
    [20 ,  9],
    [26 ,  9],
    [27 ,  9],
    [28 ,  8],
    [18 ,  7],
    [23 ,  6],
    [25 ,  6],
    [19 ,  5],
    [21 ,  4],
    [18 ,  3]
]

# Declare Solver (SCIP = Solving Constraint Integer Program)
solver = pywraplp.Solver.CreateSolver('SCIP')

# Var Defn
infinity = solver.infinity()

x = [[solver.IntVar(0.0, 1.0, f'x_{i}_{j}') for j in range(D)] for i in range(D)]

print('Number of variables =', solver.NumVariables())

# Constraints
for i,j in cities:
    constraint = 0
    for ip in range(i-3, i+Rs+1):
        for jp in range(j-3, j+Rs+1):
            if ip >= 0 and jp >= 0 and ip < D and jp < D and (i - ip)**2 + (j - jp)**2 <= Rs**2:
                constraint += x[ip][jp]

    solver.Add(constraint >= 1)

print('Number of constraints =', solver.NumConstraints())

w = [[0 for j in range(D)] for i in range(D)]

for i in range(D):
    for j in range(D):
        for ip in range(i-Rp, i+Rp+1):
            for jp in range(j-Rp, j+Rp+1):
                if ip >= 0 and jp >= 0 and ip < D and jp < D and (i - ip)**2 + (j - jp)**2 <= Rp**2:
                    w[i][j] += x[ip][jp]

# Obj
P = 0
for i in range(D):
    for j in range(D):
        P += 0.17 * w[i][j] + math.log(170)     # TODO: Fix obj function
solver.Minimize(P)

# Solve
status = solver.Solve()

# Result
if status == pywraplp.Solver.OPTIMAL:
    print('Solution:')
    print('Objective value =', solver.Objective().Value())
    for i in range(D):
        for j in range(D):
            if x[i][j].solution_value() > 0:
                print(f"({i},{j})")
else:
    print('The problem does not have an optimal solution.')


# Current Output on small.in:
# (1,23)
# (2,29)
# (7,19)
# (9,26)
# (18,4)
# (23,9)
# (27,4)
# (29,9)
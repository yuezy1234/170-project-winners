from typing import Callable, Dict

from point import Point
from instance import Instance
from solution import Solution

from ortools.linear_solver import pywraplp
import math

import numpy as np
import cvxpy as cp

# Inputs
# D = 30
# N = 25
# Rs = 3
# Rp = 8
# cities = [
#     [0  , 28],
#     [4  , 28],
#     [2  , 27],
#     [6  , 26],
#     [1  , 25],
#     [7  , 24],
#     [9  , 23],
#     [3  , 23],
#     [3  , 21],
#     [8  , 21],
#     [6  , 19],
#     [9  , 18],
#     [23 , 12],
#     [28 , 11],
#     [22 , 10],
#     [20 ,  9],
#     [26 ,  9],
#     [27 ,  9],
#     [28 ,  8],
#     [18 ,  7],
#     [23 ,  6],
#     [25 ,  6],
#     [19 ,  5],
#     [21 ,  4],
#     [18 ,  3]
# ]

def cvx_solver(instance: Instance) -> Solution:

    D = instance.D
    N = instance.N
    Rs = instance.R_s
    Rp = instance.R_p
    cities = instance.cities

    # Declare Solver (SCIP = Solving Constraint Integer Program)
    

    # x = [[solver.IntVar(0.0, 1.0, f'x_{i}_{j}') for j in range(D)] for i in range(D)]
    x = cp.Variable((D, D))
    print('Number of variables =', D * D)

    # Constraints
    constraints = []
    for p in cities:
        i, j = p.x, p.y
        constraint = 0
        for ip in range(i-Rs, i+Rs+1):
            for jp in range(j-Rs, j+Rs+1):
                if ip >= 0 and jp >= 0 and ip < D and jp < D and (i - ip)**2 + (j - jp)**2 <= Rs**2:
                    constraint += x[ip][jp]

        constraints.append(constraint >= 1)

    constraints.append(x >= np.zeros((D, D)))
    constraints.append(x <= np.ones((D, D)))
    w = cp.Variable((D, D))

    for i in range(D):
        for j in range(D):
            constraint = 0
            for ip in range(i-Rp, i+Rp+1):
                for jp in range(j-Rp, j+Rp+1):
                    if ip >= 0 and jp >= 0 and ip < D and jp < D and (i - ip)**2 + (j - jp)**2 <= Rp**2:
                        constraint += x[ip][jp]
            constraints.append(w[i][j] >= constraint)
            
    print('Number of constraints =', len(constraints))

    # Obj
    P = 0
    for i in range(D):
        for j in range(D):
            P += 170 * cp.exp(x[i][j] + 0.17 * w[i][j])     # TODO: Fix obj function
    socp = cp.Problem(cp.Minimize(P), constraints)

    # Solve
    socp.solve()
    if socp.status not in ["infeasible", "unbounded"]:
        opt_ans = [[1, 28], [1, 22], [9, 26], [8, 18], [16, 5], [24, 4], [20, 12], [28, 11]]
        # Result
        # print("Penalty achieved:", P.value)
        print([x.value[i[0]][i[1]] for i in opt_ans])
        # print(x.value)
        sol = Solution(instance=instance,
                        towers=[Point(x=i,y=j) for i in range(D) for j in range(D) if x.value[i][j]>0.5])
    else:
        print("FAILED")
        sol = None
    return sol


# Current Output on small.in:
# (1,23)
# (2,29)
# (7,19)
# (9,26)
# (18,4)
# (23,9)
# (27,4)
# (29,9)
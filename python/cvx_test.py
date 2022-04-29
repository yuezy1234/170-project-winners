import numpy as np
import cvxpy as cp
import math

# D = 3
# cities = [[0, 0], [0, 2], [2, 0], [2, 2]]
# Rs = 1
# Rp = 2

# x = cp.Variable((D, D))
# constraints = []

# for city in cities:
#     i, j = city[0], city[1]
#     constraint = 0
#     for ip in range(i-Rs, i+Rs+1):
#         for jp in range(j-Rs, j+Rs+1):
#             if ip >= 0 and jp >= 0 and ip < D and jp < D and (i - ip)**2 + (j - jp)**2 <= Rs**2:
#                 constraint += x[ip][jp]
#     constraints.append(constraint >= 1)

# print(constraints)

# w = cp.Variable((D, D))

# constraints.append(w[0][0] >= x[0][1] + x[1][0])
# for i in range(D):
#     for j in range(D):
#         constraints.append(x[i][j] >= 0)
#         constraints.append(x[i][j] <= 1)
#         constraints.append(w[i][j] >= 0)


# # Obj
# P = 0
# for i in range(D):
#     for j in range(D):
#         P += cp.multiply(x[i][j], cp.exp(w[i][j]))

# socp = cp.Problem(cp.Minimize(P), constraints)

# # Solve
# socp.solve()
# if socp.status not in ["infeasible", "unbounded"]:
#     print(x.value)
# else:
#     print("FAILED")

x = cp.Variable()
y = cp.Variable()

P = cp.exp(x + y) - cp.exp(y)
constraints = []
constraints.append(x >= 0)
constraints.append(y >= 0)

cp.Problem(cp.Minimize(P), constraints).solve()
print(x.value, y.value)

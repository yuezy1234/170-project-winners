from point import Point
from instance import Instance
from solution import Solution

import numpy as np

def squares_in_coverage(x, y, D):
    delta = [[-2, 2], [-1, 2], [0, 2], [1, 2], [2, 2],
                [-2, 1], [-1, 1], [0, 1], [1, 1], [2, 1],
                [-2, 0], [-1, 0], [0, 0], [1, 0], [2, 0],
                [-2, -1], [-1, -1], [0, -1], [1, -1], [2, -1],
                [-2, -2], [-1, -2], [0, -2], [1, -2], [2, -2],
                [-3, 0], [3, 0], [0, -3], [0, 3]
    ]
    possible = [(x + d[0], y + d[1]) for d in delta]
    return list(filter(lambda loc : 0 <= loc[0] < D and 0 <= loc[1] < D, possible))

# Return the first index of a FALSE value in an array. If none exists, return -1
def first_false_index(arr):
    for i in range(len(arr)):
        if arr[i] == False:
            return i
    return -1

# For a given tower, return indices of all uncovered cities in increasing order. 
def city_covered_indices(x, y, D, city_indices, subprob):
    indices = []
    squares_covered = squares_in_coverage(x, y, D)
    for square in squares_covered:
        if square in city_indices:
            index = city_indices[square]
            if subprob[index] == False:
                indices.append(index)
    indices.sort()
    return tuple(indices)

def greedy_solver_2d(instance: Instance) -> Solution:
    D = instance.D
    N = instance.N
    Rs = instance.R_s
    Rp = instance.R_p
    towers = []
    cities = [(city.x, city.y) for city in instance.cities]
    city_indices = {} # Maps city location to its index in list
    for i in range(N):
        city_indices[cities[i]] = i

    cities_tracker = np.zeros(N, dtype=bool) # False for not covered

    subprob_sol = {} # Key: subproblem. Value: array of different tower sequences that can reach the subproblem

    # SUBPROB: array of length N, True if city is covered. TOWERS_USED: number of towers (or sequence of tower paths) needed to get to this point.
    def recurse(subprob, towers_used):
        nonlocal subprob_sol
        target_city = cities[first_false_index(subprob)]
        resulting_change = {}
        for tower_candidate in squares_in_coverage(target_city[0], target_city[1], D):
            towers_covered = city_covered_indices(tower_candidate[0], tower_candidate[1], D, city_indices, subprob)
            if not towers_covered in resulting_change:
                resulting_change[towers_covered] = tower_candidate
        return
    
    recurse(cities_tracker, 0)

    tower_sol = [Point(x = tower[0], y = tower[1]) for tower in towers]
    sol = Solution(instance=instance,
                            towers=tower_sol)
    return sol
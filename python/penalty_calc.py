from instance import Instance
from solution import Solution
from point import Point
import math

# tower = [
#     [2, 29],
#     [1, 22],
#     [9, 26],
#     [8, 18],
#     [16, 5],
#     [24, 4],
#     [20, 12],
#     [28, 11]
# ]

tower = [
    [1, 28],
    [1, 22],
    [9, 26],
    [8, 18],
    [16, 5],
    [24, 4],
    [20, 12],
    [28, 11]
]
towers = [Point(i,j) for i,j in tower]

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

penalty_radius=8
instance = Instance(grid_side_length=30, coverage_radius=3, penalty_radius=8, cities=cities)

penalty = 0
for fidx, first in enumerate(towers):
    num_overlaps = 0
    for sidx, second in enumerate(towers):
        if fidx == sidx:
            continue
        if Point.distance_obj(first, second) <= penalty_radius:
            num_overlaps += 1
    penalty += 170 * math.exp(0.17 * num_overlaps)

print(penalty)
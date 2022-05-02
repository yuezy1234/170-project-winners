from point import Point
from instance import Instance
from solution import Solution

def small_127(instance: Instance) -> Solution:
    towers = [
        [15, 16],
        [15, 0],
        [3, 12],
        [27, 12],
        [3, 17],
        [27, 17],
        [10, 21],
        [20, 21],
        [3, 22],
        [27, 22],
        [11, 29],
        [19, 29]
    ]
    return Solution(instance=instance, towers=[Point(x = tower[0], y = tower[1]) for tower in towers])
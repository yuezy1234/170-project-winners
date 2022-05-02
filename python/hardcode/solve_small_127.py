from point import Point
from instance import Instance
from solution import Solution

def small_127(instance: Instance) -> Solution:
    towers = [
        [1, 7],
        [1, 21],
        [6, 14],
        [6, 25],
        [13, 18],
        [15, 0],
        [15, 10],
        [15, 27],
        [17, 18],
        [24, 25],
        [24, 14],
        [29, 21],
        [29, 7]
    ]
    return Solution(instance=instance, towers=[Point(x = tower[0], y = tower[1]) for tower in towers])
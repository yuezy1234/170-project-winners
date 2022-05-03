from point import Point
from instance import Instance
from solution import Solution

def large_196(instance: Instance) -> Solution:
    towers = [[51, 0]]
    for i in range(6):
        for j in range(17):
            towers.append([2 + 8 * i, 1 + 6 * j])
    return Solution(instance=instance, towers=[Point(x = tower[0], y = tower[1]) for tower in towers])
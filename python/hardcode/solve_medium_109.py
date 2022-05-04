from point import Point
from instance import Instance
from solution import Solution

def medium_109(instance: Instance) -> Solution:
    towers = []
    for i in range(13):
        towers.append([6, 1 + 4 * i])
        towers.append([44, 1 + 4 * i])
    return Solution(instance=instance, towers=[Point(x = tower[0], y = tower[1]) for tower in towers])
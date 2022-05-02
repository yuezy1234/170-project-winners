from point import Point
from instance import Instance
from solution import Solution

def large_089(instance: Instance) -> Solution:
    coords = []
    for i in range(0, 5):
        coords.append([1 + 12 * i, 99 - 24 * i])
    for i in range(0, 4):
        coords.append([5 + 12 * i, 85 - 24 * i])
        coords.append([4 + 12 * i, 93 - 24 * i])
        coords.append([8 + 12 * i, 79 - 24 * i])

    for coord in coords[:]:
        coords.append([coord[0] + 49, coord[1]])

    for i in range(0, 5):
        coords.append([72 - 12 * i, 0 + 24 * i])
    for i in range(0, 4):
        coords.append([68 - 12 * i, 14 + 24 * i])
        coords.append([69 - 12 * i, 6 + 24 * i])
        coords.append([65 - 12 * i, 20 + 24 * i])
    
    coords.extend([
        [0, 52], [12, 28], [24, 4],
        [3, 46], [15, 22],
        [6, 39], [18, 15], 
        [9, 33], [21, 9],

        [75, 98], [87, 74], [99, 50],
        [81, 85], [93, 61],
        [78, 92], [90, 68],
        [84, 79], [96, 55],

        [0, 0], [99, 99]
    ])

    coords.sort()
    print(coords)

    return Solution(instance=instance, towers=[Point(x = coord[0], y = coord[1]) for coord in coords])

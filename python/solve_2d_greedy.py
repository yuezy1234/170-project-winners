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
    possible = [[x + d[0], y + d[1]] for d in delta]
    return list(filter(lambda loc : 0 <= loc[0] < D and 0 <= loc[1] < D, possible))

def greedy_solver_2d(instance: Instance) -> Solution:
    D = instance.D
    N = instance.N
    Rs = instance.R_s
    Rp = instance.R_p
    
    towers = []
    cities = [[city.x, city.y] for city in instance.cities]

    cities_in_range = np.zeros((D, D))
    for city in cities:
        for square in squares_in_coverage(city[0], city[1], D):
            cities_in_range[square[0]][square[1]] += 1
    cities_left = N
    while cities_left > 0:
        target_city = cities[0]
        greedy_tower = None
        max_cities_covered = 0
        
        # Greedily choose the tower that covers the top-most city and as many others as possible
        for tower_candidate in squares_in_coverage(target_city[0], target_city[1], D):
            if cities_in_range[tower_candidate[0]][tower_candidate[1]] > max_cities_covered:
                greedy_tower = tower_candidate
                max_cities_covered = cities_in_range[tower_candidate[0]][tower_candidate[1]]
        towers.append(greedy_tower)
        
        for square in squares_in_coverage(greedy_tower[0], greedy_tower[1], D):
            city_x = square[0]
            city_y = square[1]
            if square in cities:
                cities.remove(square)
                cities_left -= 1
                for city_neighbor in squares_in_coverage(city_x, city_y, D):
                    cities_in_range[city_neighbor[0]][city_neighbor[1]] -= 1
    tower_sol = [Point(x = tower[0], y = tower[1]) for tower in towers]
    sol = Solution(instance=instance,
                            towers=tower_sol)
    for i in range(1):
        print(f"-------Attempt #{i} ---------")
        sol.anneal()
    return sol

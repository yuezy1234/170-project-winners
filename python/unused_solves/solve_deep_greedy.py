from typing import Callable, Dict

from point import Point
from instance import Instance
from solution import Solution

import math
import numpy as np

import multiprocessing as mp

city_award = 5
tower_penalty = -4
donut_penalty = -3

def squares_in_range(x, y, radius, D):
    squares = []
    for xp in range(x-radius, x+radius+1):
        for yp in range(y-radius, y+radius+1):
            if xp >= 0 and yp >= 0 and xp < D and yp < D and (x - xp)**2 + (y - yp)**2 <= radius**2:
                squares.append([xp, yp])
    return squares

def donut_in_range(x, y, inner, outer, D):
    squares = []
    for xp in range(x-outer, x+outer+1):
        for yp in range(y-outer, y+outer+1):
            if xp >= 0 and yp >= 0 and xp < D and yp < D and (x - xp)**2 + (y - yp)**2 <= outer**2 and (x - xp)**2 + (y - yp)**2 > inner**2:
                squares.append([xp, yp])
    return squares

def run_greedy_deep(tmap, cmap, cities, towers, donuts, cities_left, depth, instance):
    _tmap = tmap.copy()
    _cmap = cmap.copy()
    _cities = cities.copy()
    _towers = towers.copy()
    _donuts = donuts.copy()
    _cities_left = cities_left

    D = instance.D
    N = instance.N
    Rs = instance.R_s
    Rp = instance.R_p
    inst_cities = instance.cities

    best_rating_square = [0, 0]
    best_rating = -float("inf")

    if depth == 0 or cities_left <= 0:
        return [0,0]

    for x in range(D):
        for y in range(D):

            if _tmap[x][y] ==  0 and _cities[x][y] > 0:
                # calc curr rating
                current_rating = city_award * _cities[x][y] \
                    + tower_penalty * _towers[x][y] \
                    + donut_penalty * _donuts[x][y]
                # print(current_rating)
                

                # update arrays
                _tmap[x][y] = 1
                for square in squares_in_range(x, y, Rs, D):
                    city_x, city_y = square[0], square[1]
                    if _cmap[city_x][city_y] == 1:
                        _cmap[city_x][city_y] = 0
                        _cities_left -= 1
                        for city_neighbor in squares_in_range(city_x, city_y, Rs, D):
                            _cities[city_neighbor[0]][city_neighbor[1]] -= 1
                        for city_neighbor in donut_in_range(city_x, city_y, Rs, Rp, D):
                            _donuts[city_neighbor[0]][city_neighbor[1]] -= 1
                for square in squares_in_range(x, y, Rp, D):
                    _towers[square[0]][square[1]] += 1

                # recurse
                current_rating += run_greedy_deep(_tmap, _cmap, _cities, _towers, _donuts, \
                                                  _cities_left, depth-1, instance)[1]

                # print(current_rating)

                # update rating
                if current_rating > best_rating:
                    best_rating_square = [x, y]
                    best_rating = current_rating

                # restore arrays
                _tmap = tmap.copy()
                _cmap = cmap.copy()
                _cities = cities.copy()
                _towers = towers.copy()
                _donuts = donuts.copy()
                _cities_left = cities_left
            
                if depth == 2:
                    print(f"Rating for ({x}, {y}): {current_rating}")
    
    return best_rating_square, best_rating


def deep_greedy_solver(instance: Instance) -> Solution:

    D = instance.D
    N = instance.N
    Rs = instance.R_s
    Rp = instance.R_p
    cities = instance.cities

    towers_map = np.zeros((D, D)) # Boolean of whether there is a tower there
    cities_in_range = np.zeros((D, D)) # Tracks the number of cities in range on each square
    towers_in_range = np.zeros((D, D)) # Tracks the penalty on each square
    donuts_in_range = np.zeros((D, D))
    # rating_tracker = np.array((D, D)) # Tracks the rating for each square, puts a tower at the maximum one (greedy)

    greedy_depth = 2

    city_map = np.zeros((D, D))
    cities_left =  0
    for city in cities:
        x, y = city.x, city.y
        cities_left += 1
        city_map[x][y] += 1
        for square in squares_in_range(x, y, Rs, D):
            cities_in_range[square[0]][square[1]] += 1
        for square in donut_in_range(x, y, Rs, Rp, D):
            donuts_in_range[square[0]][square[1]] += 1

    # city_award = 5
    # tower_penalty = -4
    # donut_penalty = -3

    while cities_left > 0:
        
        best_rating_square, best_rating = \
            run_greedy_deep(towers_map, city_map, cities_in_range, towers_in_range, \
                            donuts_in_range, cities_left, greedy_depth, instance)
        
        print(f"Choosing {best_rating_square}: {best_rating}")
        
        x = best_rating_square[0]
        y = best_rating_square[1]
        towers_map[x][y] = 1
        # print(f"built tower at {x}, {y} with a score of {best_rating}")
        # print(cities_in_range[x][y], towers_in_range[x][y], donuts_in_range[x][y])
        for square in squares_in_range(x, y, Rs, D):
            city_x = square[0]
            city_y = square[1]
            if city_map[city_x][city_y] == 1:
                city_map[city_x][city_y] = 0
                cities_left -= 1
                for city_neighbor in squares_in_range(city_x, city_y, Rs, D):
                    cities_in_range[city_neighbor[0]][city_neighbor[1]] -= 1
                for city_neighbor in donut_in_range(city_x, city_y, Rs, Rp, D):
                    donuts_in_range[city_neighbor[0]][city_neighbor[1]] -= 1
        for square in squares_in_range(x, y, Rp, D):
            towers_in_range[square[0]][square[1]] += 1
        
    sol = Solution(instance=instance,
                        towers=[Point(x=i,y=j) for i in range(D) for j in range(D) if towers_map[i][j]>0])

    return sol
    
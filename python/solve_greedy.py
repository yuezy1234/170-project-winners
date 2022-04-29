from typing import Callable, Dict

from point import Point
from instance import Instance
from solution import Solution

import math
import numpy as np

import time

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

def greedy_solver(instance: Instance) -> Solution:
    best_sol = None
    best_penalty = float("inf")
    for iter in range(10000):
        # if iter % 1000 == 0: print(iter)
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

        city_map = np.zeros((D, D))
        cities_left =  0
        for city in cities:
            x, y= city.x, city.y
            cities_left += 1
            city_map[x][y] += 1
            for square in squares_in_range(x, y, Rs, D):
                cities_in_range[square[0]][square[1]] += 1
            for square in donut_in_range(x, y, Rs, Rp-Rs, D):
                donuts_in_range[square[0]][square[1]] += 1

        city_award = 10
        tower_penalty = -3
        donut_penalty = -5

        while cities_left > 0:
            # best_rating_square = [0, 0]
            # best_rating = -float("inf")

            prob = []
            points = []

            for x in range(D):
                for y in range(D):
                    if towers_map[x][y] == 0 and cities_in_range[x][y] > 0:
                        current_rating = city_award * cities_in_range[x][y] \
                            + tower_penalty * math.exp(towers_in_range[x][y]) \
                            + donut_penalty * donuts_in_range[x][y]

                        prob.append(current_rating)
                        points.append(Point(x,y))

                        # if current_rating > best_rating:
                        #     best_rating_square = [x, y]
                        #     best_rating = current_rating
            # print(prob)
            # print("Max:", max(prob))
            # print("Pre (1,28):", prob[ind_1_28])
            # print("Pre (6,23):", prob[ind_6_23])
            prob = np.array(prob)
            prob = prob - np.min(prob)
            # print("After shift")
            # print(prob)
            tops = prob > (0.8 * max(prob))
            prob = (prob * tops) 
            # print(prob)
            # print(np.sum(prob))
            if not np.sum(prob) == 0:
                prob = prob / np.sum(prob)
            else:
                prob = None
            # print(prob)
            # print("Post (28,11):", prob[ind_28_11])
            # print("Post (25,8):", prob[ind_25_8])
            # print("Post (18,4):", prob[ind_18_4])
            selected_point = np.random.choice(points, p=prob)
            x, y = selected_point.x, selected_point.y
            # print("Distr:", np.sort(prob))
            # print("Points:", [(p.x,p.y) for p in points])
            # print(f"Choosing ({x}, {y}) wp {prob[points.index(selected_point)]}")
            # x = best_rating_square[0]
            # y = best_rating_square[1]
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
                    for city_neighbor in donut_in_range(city_x, city_y, Rs, Rp-Rs, D):
                        donuts_in_range[city_neighbor[0]][city_neighbor[1]] -= 1
            for square in squares_in_range(x, y, Rp, D):
                towers_in_range[square[0]][square[1]] += 1
            
        
        tower_sol = [Point(x=i,y=j) for i in range(D) for j in range(D) if towers_map[i][j]>0]
        sol = Solution(instance=instance,
                            towers=tower_sol)
        
        curr_penalty = sol.penalty()
        if curr_penalty < best_penalty:
            best_sol = sol
            best_penalty = curr_penalty

        # if sol.penalty() < 1600:
        #     print(sol.penalty())
        #     print([(i,j) for i in range(D) for j in range(D) if towers_map[i][j]>0])
        #     break

        # if sol.penalty() < 1960:
        #     break
    return best_sol
    
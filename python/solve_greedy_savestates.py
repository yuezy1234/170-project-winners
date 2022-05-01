from cmath import inf
from point import Point
from instance import Instance
from solution import Solution

import numpy as np
import os

greedy_dir = 'out_greedy_dir'

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

def greedy_solver_savestates(instance: Instance) -> Solution:
    D = instance.D
    N = instance.N
    Rs = instance.R_s
    Rp = instance.R_p
    
    best_sol = None
    min_towers = N * 2

    best_sols = []

    
    failure_threshold = N * 10
    if D == 30:
        greedy_iter_multiplier = 400
        max_tolerance_divider = 2
        anneal_attempts = 20
    elif D == 50:
        greedy_iter_multiplier = 200
        max_tolerance_divider = 4
        anneal_attempts = 10
    else:
        greedy_iter_multiplier = 50
        max_tolerance_divider = 8
        anneal_attempts = 5
    greedy_iter_num = N * greedy_iter_multiplier
    

    tower_sequences = [] # Array of sequences of towers
    subprob_sol = {} # Key: subproblem. Value: [min steps to reach this subproblem, array of OUTCOMES]
    
    for i in range(greedy_iter_num):
        if i % 500 == 0:
            print(f"Greedy iteration {i}")
        tolerance = (i % (greedy_iter_num // max_tolerance_divider)) / greedy_iter_num
        towers = []
        cities_tracker = np.zeros(N, dtype=bool) # False for not covered

        cities = [(city.x, city.y) for city in instance.cities]
        city_indices = {} # Maps city location to its index in list
        for i in range(N):
            city_indices[cities[i]] = i

        cities_in_range = np.zeros((D, D), dtype=int)
        for city_index in cities:
            for square in squares_in_coverage(city_index[0], city_index[1], D):
                cities_in_range[square[0]][square[1]] += 1
        
        cities_left = N
        failures = 0
        while cities_left > 0 and failures < failure_threshold:
            curr_subprob = tuple(cities_tracker)
            if curr_subprob in subprob_sol and subprob_sol[curr_subprob][0] < len(towers):
                failures += 1
                continue # If we have seen the subproblem before and did better last time, just skip
            
            target_city_index = first_false_index(cities_tracker)

            if target_city_index == -1:
                break  

            if curr_subprob not in subprob_sol:
                target_city = cities[target_city_index]
                max_cities_covered = 0
                resulting_change = {} # Key: tuple of indices of uncovered cities. Value: location of tower that can cover it.
                # Greedily choose the tower that covers the top-most city and as many others as possible
                for tower_candidate in squares_in_coverage(target_city[0], target_city[1], D):
                    towers_covered = city_covered_indices(tower_candidate[0], tower_candidate[1], D, city_indices, curr_subprob)
                    if not towers_covered in resulting_change:
                        resulting_change[towers_covered] = tower_candidate
                    if cities_in_range[tower_candidate[0]][tower_candidate[1]] > max_cities_covered:
                        max_cities_covered = cities_in_range[tower_candidate[0]][tower_candidate[1]]
                outcomes = [] # The ith element contains all pairs [new_city_indices, tower location that achieves that]
                for _ in range(max_cities_covered + 1): 
                    outcomes.append([])
                for new_city_indices in resulting_change:
                    outcomes[len(new_city_indices)].append([new_city_indices, resulting_change[new_city_indices]])
                subprob_sol[curr_subprob] = [len(towers), outcomes]
            else:
                outcomes = subprob_sol[curr_subprob][1]
                if len(towers) < subprob_sol[curr_subprob][0]:
                    subprob_sol[curr_subprob][0] = len(towers)

            # print(outcomes)
            max_covering_size = len(outcomes) - 1
            if np.random.rand() > tolerance:
                covering_size_chosen = max_covering_size # Choosing from the max
            else:
                size_distribution = np.zeros(len(outcomes))
                for i in range(1, len(outcomes)):
                    size_distribution[i] += i * len(outcomes[i])
                covering_size_chosen = np.random.choice(np.arange(len(outcomes)), p=size_distribution / np.sum(size_distribution))
            
            index_given_size = np.random.choice(len(outcomes[covering_size_chosen]))
            outcome_chosen = outcomes[covering_size_chosen][index_given_size]
            cities_chosen = outcome_chosen[0]
            tower_chosen = outcome_chosen[1]
            towers.append(tower_chosen)
            # print(f"Tower at {tower_chosen}, covering cities {cities_chosen}")

            for city_index in cities_chosen:
                cities_tracker[city_index] = True
                city_square = cities[city_index]
                cities_left -= 1
                for city_neighbor in squares_in_coverage(city_square[0], city_square[1], D):
                    cities_in_range[city_neighbor[0]][city_neighbor[1]] -= 1
        # if failures >= failure_threshold:
        #     print(f"{iter_num}: Unsuccessful find with tolerance {tolerance}")
        if cities_left == 0:
            tower_sequences.append(towers)
            tower_sol = [Point(x = tower[0], y = tower[1]) for tower in towers]
            sol = Solution(instance=instance,
                                towers=tower_sol)
            pen = sol.penalty()
            # print(f"{iter_num}: Found length {len(towers)} with tolerance {tolerance}. Penalty: {pen}")
            if len(towers) < min_towers or (len(towers) == min_towers and pen < best_sol.penalty()):
                best_sol = sol
                min_towers = len(towers)
                best_sol_towers = tower_sol

            best_sols.append(sol)

                
    print(f"Towers: {min_towers}")
    print(f"Penalty: {best_sol.penalty()}")
    
    best_sols = sorted(best_sols, key=lambda s: (len(s.towers), s.penalty()))


    for idx, s in enumerate(best_sols[:3]):
        fout = os.path.join(greedy_dir, instance.size, str(instance.num) + '_' + str(idx) + '.greedy')
        with open(fout, 'w') as f:
            s.serialize(f)

    best_anneal_penalty = float("inf")
    best_anneal_sol = None
    for i in range(anneal_attempts):
        anneal_sol = Solution(instance=instance, towers=best_sol_towers)
        print(f"Anneal attempt {i}")
        anneal_sol.anneal()
        print(anneal_sol.penalty())
        
        curr_penalty = anneal_sol.penalty()
        if curr_penalty < best_anneal_penalty:
            best_anneal_sol = anneal_sol
            best_anneal_penalty = curr_penalty
            with instance.sol_outf.open('w') as g:
                best_sol.serialize(g)
    return best_anneal_sol

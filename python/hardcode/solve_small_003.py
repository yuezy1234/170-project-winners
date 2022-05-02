from point import Point
from instance import Instance
from solution import Solution

anneal_attempts = 1000

def small_003(instance: Instance) -> Solution:
    cities = instance.cities
    towers = [Point(city.x, city.y) for city in cities]
    sol = Solution(instance=instance, towers=towers)

    best_anneal_penalty = float("inf")
    best_anneal_sol = None
    print("Before anneal:", sol.penalty())
    for i in range(anneal_attempts):
        anneal_sol = Solution(instance=instance, towers=sol.towers[:])
        print(f"===Anneal attempt {i}===")
        anneal_sol.anneal()
        print(anneal_sol.penalty())
        
        curr_penalty = anneal_sol.penalty()
        if curr_penalty < best_anneal_penalty:
            print("NEW BEST!")
            best_anneal_sol = anneal_sol
            best_anneal_penalty = curr_penalty
            with instance.sol_outf.open('w') as g:
                best_anneal_sol.serialize(g)
    print("Best anneal sol: ", best_anneal_sol.penalty())
    return best_anneal_sol
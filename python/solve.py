"""Solves an instance.

Modify this file to implement your own solvers.

For usage, run `python3 solve.py --help`.
"""

import argparse
from pathlib import Path
from typing import Callable, Dict

from instance import Instance
from solution import Solution
from file_wrappers import StdinFileWrapper, StdoutFileWrapper

from unused_solves.solve_ilp import ilp_solver
from unused_solves.solve_cvx import cvx_solver
from solve_greedy import greedy_solver
from unused_solves.solve_deep_greedy import deep_greedy_solver
from solve_2d_greedy import greedy_solver_2d
from solve_greedy_savestates import greedy_solver_savestates
from hardcode.solve_large_089 import large_089
from hardcode.solve_small_127 import small_127
from hardcode.solve_small_003 import small_003
from solve_greedy_savestates_random import greedy_solver_savestates_random
from hardcode.solve_large_196 import large_196
from hardcode.solve_medium_109 import medium_109

def solve_naive(instance: Instance) -> Solution:
    return Solution(
        instance=instance,
        towers=instance.cities,
    )

def solve_ilp(instance: Instance) -> Solution:
    return ilp_solver(instance)

def solve_cvx(instance: Instance) -> Solution:
    return cvx_solver(instance)

def solve_greedy(instance: Instance) -> Solution:
    return greedy_solver(instance)

def solve_deep_greedy(instance: Instance) -> Solution:
    return deep_greedy_solver(instance)

def solve_greedy_2d(instance: Instance) -> Solution:
    return greedy_solver_2d(instance)

def solve_greedy_savestates(instance: Instance) -> Solution:
    return greedy_solver_savestates(instance)

def solve_large_089(instance: Instance) -> Solution:
    return large_089(instance)

def solve_small_127(instance: Instance) -> Solution:
    return small_127(instance)

def solve_small_003(instance: Instance) -> Solution:
    return small_003(instance)

def solve_greedy_savestates_random(instance: Instance) -> Solution:
    return greedy_solver_savestates_random(instance)

def solve_large_196(instance: Instance) -> Solution:
    return large_196(instance)

def solve_medium_109(instance: Instance) -> Solution:
    return medium_109(instance)

SOLVERS: Dict[str, Callable[[Instance], Solution]] = {
    "naive": solve_naive, 
    "ilp": solve_ilp,
    "cvx": solve_cvx,
    "greedy": solve_greedy,
    "deep_greedy": solve_deep_greedy,
    "greedy_2d": solve_greedy_2d,
    "greedy_ss": solve_greedy_savestates,
    "large_089": solve_large_089,
    "small_127": solve_small_127,
    "small_003": solve_small_003,
    "greedy_ssr": solve_greedy_savestates_random,
    "large_196": solve_large_196, 
    "medium_109": solve_medium_109
}


# You shouldn't need to modify anything below this line.
def infile(args):
    if args.input == "-":
        return StdinFileWrapper()

    return Path(args.input).open("r")


def outfile(args):
    if args.output == "-":
        return StdoutFileWrapper()

    return Path(args.output).open("w")


def main(args):
    with infile(args) as f:
        instance = Instance.parse(f.readlines())
        inf = Path(args.input)
        instance.num = int(inf.stem)
        instance.size = inf.parent.stem
        instance.sol_outf = Path(args.output)
        solver = SOLVERS[args.solver]
        solution = solver(instance)
        assert solution.valid()
        with outfile(args) as g:
            # print("# Penalty: ", solution.penalty(), file=g)
            solution.serialize(g)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve a problem instance.")
    parser.add_argument("input", type=str, help="The input instance file to "
                        "read an instance from. Use - for stdin.")
    parser.add_argument("--solver", required=True, type=str,
                        help="The solver type.", choices=SOLVERS.keys())
    parser.add_argument("output", type=str,
                        help="The output file. Use - for stdout.",
                        default="-")
    main(parser.parse_args())

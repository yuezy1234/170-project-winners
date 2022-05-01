from __future__ import annotations

import dataclasses
import math
from typing import Iterable, List, Dict, TYPE_CHECKING

import parse
from instance import Instance
from point import Point
from svg import SVGGraphic

if TYPE_CHECKING:
    from visualize import VisualizationConfig

import numpy as np

@dataclasses.dataclass
class Solution:
    towers: List[Point]
    instance: Instance

    def valid(self):
        """Determines whether a solution is valid.

        A solution is valid for a problem instance if its towers cover all
        cities in the instance, all towers are in bounds, and there are no
        duplicate towers.
        """
        for tower in self.towers:
            if not 0 <= tower.x < self.instance.grid_side_length:
                print(f"city at {tower.x}, {tower.y} not in x bound")
                return False
            if not 0 <= tower.y < self.instance.grid_side_length:
                print(f"city at {tower.x}, {tower.y} not in y bound")
                return False

        for city in self.instance.cities:
            for tower in self.towers:
                if Point.distance_obj(city, tower) <= self.instance.coverage_radius:
                    break
            else:
                print(f"no tower covering city at {city.x}, {city.y}")
                return False

        return len(set(self.towers)) == len(self.towers)

    def deduplicate(self):
        """Removes duplicate towers from the solution."""
        # Use dict to preserve tower order.
        self.towers = list({tower: () for tower in self.towers}.keys())

    def penalty(self):
        """Computes the penalty for this solution."""
        penalty = 0
        self.tower_overlap = np.zeros(len(self.towers))
        for fidx, first in enumerate(self.towers):
            num_overlaps = 0
            for sidx, second in enumerate(self.towers):
                if fidx == sidx:
                    continue
                if Point.distance_obj(first, second) <= self.instance.penalty_radius:
                    num_overlaps += 1
            self.tower_overlap[fidx] = num_overlaps
            penalty += 170 * math.exp(0.17 * num_overlaps)
        return penalty

    @staticmethod
    def parse(lines: Iterable[str], instance: Instance):
        lines_iter = parse.remove_comments(lines)
        num_towers_s = next(lines_iter, None)
        assert num_towers_s is not None
        num_towers = int(num_towers_s)

        towers = []
        for line in lines_iter:
            towers.append(Point.parse(line))
        assert num_towers == len(towers)

        sol = Solution(towers=towers, instance=instance)
        assert sol.valid()
        return sol

    def serialize(self, out):
        print("# Penalty: ", self.penalty(), file=out)
        print(len(self.towers), file=out)
        for tower in self.towers:
            print(tower.x, tower.y, file=out)

    def serialize_to_string(self) -> str:
        return parse.serialize_to_string_impl(self.serialize, self)

    def visualize_as_svg(self, config: VisualizationConfig) -> SVGGraphic:
        out = self.instance.visualize_as_svg(config)

        def _rescale(x):
            return x / self.instance.grid_side_length * config.size

        def _draw_circle(pt, radius, color, opacity):
            out.draw_circle(
                _rescale(pt.x),
                _rescale(pt.y),
                _rescale(radius),
                0,
                color,
                opacity=opacity,
            )

        for tower in self.towers:
            out.draw_circle(
                _rescale(tower.x),
                _rescale(tower.y),
                2,
                0,
                config.tower_color,
            )
            _draw_circle(
                tower,
                self.instance.coverage_radius,
                config.coverage_color,
                config.coverage_opacity,
            )
            _draw_circle(
                tower,
                self.instance.penalty_radius,
                config.penalty_color,
                config.penalty_opacity,
            )

        return out
    
    def anneal(self):
        T = 10000
        D = self.instance.D
        cities = self.instance.cities
        self.city_cover = self.cities_covered_dict()
        while T > 0.01:
            self.curr_pen = self.penalty()
            old_penalty = self.curr_pen
            if np.sum(self.tower_overlap) == 0:
                break
            tower_penalty_proportion = self.tower_overlap / np.sum(self.tower_overlap)
            # Can change to non-linear proportion
            # tower_penalty_proportion = tower_penalty_proportion ** 2 
            # tower_penalty_proportion = tower_penalty_proportion / np.sum(tower_penalty_proportion)
            # print(tower_penalty_proportion)
            tower_moved = np.random.choice(len(self.towers))
            # tower_moved = np.random.choice(len(self.towers), p=tower_penalty_proportion)
            tower_x = self.towers[tower_moved].x
            tower_y = self.towers[tower_moved].y

            curr_cities_covered = self.cities_covered(self.towers[tower_moved])

            dx = 0
            dy = 0
            while not((dx != 0 or dy != 0) and tower_x + dx >= 0 and tower_x + dx < D and tower_y + dy >= 0 and tower_y + dy < D) and Point(dx+tower_x, dy+tower_y) not in self.towers:
                x_abs = np.random.poisson(0.5) + 1
                y_abs = np.random.poisson(0.5) + 1

                dx = (np.random.randint(3) - 1) * x_abs
                dy = (np.random.randint(3) - 1) * y_abs
            
            # print(dx, dy)

            new_x = tower_x + dx
            new_y = tower_y + dy
            
            self.towers[tower_moved] = Point(new_x, new_y)
            new_cities_covered = self.cities_covered(self.towers[tower_moved])

            if new_cities_covered != curr_cities_covered:
                uncovered = curr_cities_covered.difference(new_cities_covered)
                if any([len(self.city_cover[(p.x,p.y)]) == 1 for p in uncovered]):
                    self.towers[tower_moved] = Point(tower_x, tower_y)
                    # print("QUITTING")
                    T *= 0.999
                    continue
            
            # print(f"Moving ({tower_x}, {tower_y}) to ({new_x}, {new_y})")
            # print(f"Penalty: {self.curr_pen} -> {new_penalty} (d={delta})")

            new_penalty = self.penalty()
            delta = new_penalty - self.curr_pen
            if delta <= 0:
                self.curr_pen = new_penalty
            else:
                if np.random.rand() < np.exp(-delta / T):
                    self.curr_pen = new_penalty
                else:
                    self.towers[tower_moved] = Point(tower_x, tower_y)
            # if(self.curr_pen == new_penalty and delta != 0):
                # print(f"Moving ({tower_x}, {tower_y}) to ({new_x}, {new_y})")
                # print(f"Penalty: {old_penalty} -> {new_penalty} (d={delta}, T={T})")
            # print(tower_x, tower_y, new_x, new_y)
            # print(curr_cities_covered)
            # print(new_cities_covered)
            if(self.curr_pen == new_penalty):
                for p in curr_cities_covered.difference(new_cities_covered):
                    self.city_cover[(p.x, p.y)].remove((tower_x, tower_y))
                for p in new_cities_covered.difference(curr_cities_covered):
                    self.city_cover[(p.x, p.y)].add((new_x, new_y))
                for p in curr_cities_covered.intersection(new_cities_covered):
                    # print((p.x, p.y))
                    # print(self.city_cover[(p.x, p.y)])
                    self.city_cover[(p.x, p.y)].add((new_x, new_y))
                    self.city_cover[(p.x, p.y)].remove((tower_x, tower_y))
                    # print(self.city_cover[(p.x, p.y)])

            # else:
            #     pass
            #     # print("No Move")
            T *= 0.999

    def cities_covered(self, t):
        covered = set()
        for city in self.instance.cities:
            if (city.x - t.x) ** 2 + (city.y - t.y) ** 2 <= self.instance.R_s ** 2:
                covered.add(city)
        return covered
    
    def cities_covered_dict(self):
        covered = {}
        # print(self.instance.cities)
        for city in self.instance.cities:
            covered[(city.x, city.y)] = set()
            for t in self.towers:
                if (city.x - t.x) ** 2 + (city.y - t.y) ** 2 <= self.instance.R_s ** 2:
                    covered[(city.x, city.y)].add((t.x, t.y))
        # print(covered)
        return covered

            

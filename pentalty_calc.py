towers = [
    [2, 30],
    [1, 22],
    [9, 26],
    [8, 18],
    [16, 5],
    [24, 4],
    [20, 12],
    [28, 11]
]

penalty_radius = 8

penalty = 0
for fidx, first in enumerate(towers):
    num_overlaps = 0
    for sidx, second in enumerate(towers):
        if fidx == sidx:
            continue
        if Point.distance_obj(first, second) <= penalty_radius:
            num_overlaps += 1
    penalty += 170 * math.exp(0.17 * num_overlaps)
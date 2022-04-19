import random

# Medium

shifts = [
    [0, 0],
    [20, 1],
    [39, 8],
    [8, 19],
    [0, 38],
    [27, 26],
    [39, 39],
]

originals = [
    [1, 3],
    [4, 0],
    [3, 2],
    [11, 5],
    [3, 7],
    [0, 10],
    [8, 2],
]

# Large
# shifts = [
#     [0, 0],
#     [27, 0],
#     [54, 0],
#     [81, 0],
#     [12, 24],
#     [39, 24],
#     [66, 24],
#     [1, 46],
#     [36, 53],
#     [61, 51],
#     [87, 42],
#     [13, 70],
#     [50, 73],
#     [76, 71]
# ]

# originals = [
#     [0, 3],
#     [1, 2],
#     [2, 2],
#     [2, 1],
#     [3, 0],
#     [2, 13],
#     [2, 12],
#     [3, 12],
#     [3, 13],
#     [4, 14],
#     [10, 6],
#     [11, 6],
#     [11, 5],
#     [11, 4],
#     [12, 4]
# ]

# def permutate():
#     for shift in shifts:
#         for original in originals:
#             print(original[0] + shift[0], original[1] + shift[1])

# permutate()

coords = []
for shift in shifts:
    for original in originals:
        coords.append([original[0] + shift[0], original[1] + shift[1]])

random.shuffle(coords)
for coord in coords:
    print(coord[0], coord[1])

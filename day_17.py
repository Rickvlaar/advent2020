import util
import numpy as np
import itertools

test_dimension = ['.#.',
                  '..#',
                  '###']

start_dimension = util.parse_file_as_list('input_files/day_17.txt')


def enter_the_matrix_again(dimensions=4):
    universe = np.array([[1 if char == '#' else 0 for char in line] for line in start_dimension], ndmin=dimensions)
    for loops in range(6):
        universe = expand_the_universe(universe)
    return universe.sum()


def expand_the_universe(universe):
    #  order of position in matrix is z, y, x
    z, y, x = universe.shape

    expanded_universe = np.array(np.zeros((z + 4, y + 4, x + 4)))
    expanded_universe[2: -2, 2: -2, 2: -2] = universe
    the_newlyverse = np.array(np.zeros((z + 4, y + 4, x + 4)))

    for cube_coords in itertools.product(range(1, z + 3), itertools.product(range(1, x + 3), repeat=2)):
        z, y_x = cube_coords
        y, x = y_x
        cube_value = expanded_universe[z, y, x]
        active_cube_neighbours = expanded_universe[z-1:z+2, y-1:y+2, x-1:x+2].sum() - cube_value
        if cube_value == 0 and active_cube_neighbours == 3:
            new_cube_value = 1
        elif cube_value == 1 and active_cube_neighbours in (2, 3):
            new_cube_value = 1
        else:
            new_cube_value = 0
        the_newlyverse[z, y, x] = new_cube_value
    return the_newlyverse

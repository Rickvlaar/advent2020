import util

tree_file = 'input_files/day_3.txt'
tree_file_list = util.parse_file_as_list(file=tree_file)

test_map = ['..##.......',
            '#...#...#..',
            '.#....#..#.',
            '..#.#...#.#',
            '.#...##..#.',
            '..#.##.....',
            '.#.#.#....#',
            '.#........#',
            '#.##...#...',
            '#...##....#',
            '.#..#...#.#']


def count_trees_on_slope_part_1(right, down):
    return sum([1 for index, line in enumerate(tree_file_list) if index % down == 0 and line[round(((index * right) / down)) % len(line)] == '#'])


def count_trees_on_slope_part_2():
    input_array = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    print([count_trees_on_slope_part_1(right, down) for right, down in input_array])

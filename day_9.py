import util
from itertools import product, starmap, combinations_with_replacement, accumulate
number_file = 'input_files/day_9.txt'
number_list = [int(num) for num in util.parse_file_as_list(number_file)]


def find_weakness(preamble=25):
    for index, num in enumerate(number_list):
        if index > preamble - 1:
            all_possible_permutations = {x + y for x in number_list[index - preamble:] for y in number_list[index - preamble:]}
            if num not in all_possible_permutations:
                return num


def determine_weakness(weak_num):
    combination_size = 2
    while True:
        for index, value in enumerate(number_list, combination_size):
            if sum(number_list[index - combination_size:index]) == weak_num:
                return min(number_list[index - combination_size:index]) + max(number_list[index - combination_size:index])
            index += 1
        combination_size += 1

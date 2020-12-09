import util
from itertools import starmap
number_file = 'input_files/day_9.txt'


def find_weakness(preamble=25):
    number_list = [int(num) for num in util.parse_file_as_list(number_file)]
    for index, num in enumerate(number_list):
        if index > preamble - 1:
            all_possible_permutations = {x + y for x in number_list[index - preamble:] for y in number_list[index - preamble:]}
            if num not in all_possible_permutations:
                return num

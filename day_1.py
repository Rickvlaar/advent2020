from itertools import combinations
input_file_day_1 = 'input_files/day_1_1.txt'


def is_sum_of(total=2020, combination_size=3):
    input_file = [int(num) for num in open(file=input_file_day_1, newline='\n').readlines()]
    combines_to_total = [perm for perm in combinations(input_file, r=combination_size) if sum(perm) == total]
    print(combines_to_total)

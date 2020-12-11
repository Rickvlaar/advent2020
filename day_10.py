import util
from functools import reduce
from operator import mul
adapter_file = 'input_files/day_10.txt'


def sort_adapters():
    adapter_list = [int(num) for num in util.parse_file_as_list(adapter_file)]
    adapter_list.append(0)
    adapter_list.append(max(adapter_list) + 3)
    adapter_list.sort(reverse=True)
    jolt_diffs = [adapter_list[index - 1] - adapter for index, adapter in enumerate(adapter_list) if index > 0]
    three_indices = [index for index, num in enumerate(jolt_diffs) if num == 3]
    three_indices.append(len(jolt_diffs))
    three_index_diffs = [x - three_indices[index - 1] for index, x in enumerate(three_indices) if index > 0]
    combination_dict = {5: 7, 4: 4, 3: 2, 2: 1, 1: 1}
    total_combinations = reduce(mul, [combination_dict.get(num) for num in three_index_diffs])
    return jolt_diffs.count(1), jolt_diffs.count(3), total_combinations

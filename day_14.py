import itertools
import util

program_file = util.parse_file_as_list('input_files/day_14.txt')
mem = {}


def read_program():
    bitmask = ''
    for line in program_file:
        if line.startswith('mask'):
            bitmask = line.lstrip('mask = ')
        elif line.startswith('mem'):
            address, value = line.split('] = ')
            mem_index = int(address.lstrip('mem['))
            # bin_value, original_bin_length = format_value(value, mem_index)
            bin_value = format(int(mem_index), 'b').zfill(36)
            mask_decode(bin_value, bitmask, value)
            # masked_bin_value = apply_mask(bin_value, bitmask)
            # mem[mem_index] = masked_bin_value
    return sum([int(value) for value in mem.values()])


def format_value(bin_value, mem_index):
    bin_value = format(int(bin_value), 'b')
    original_bin_length = len(bin_value)
    if len(bin_value) < 36 - mem_index:
        needed_pad = 36 - mem_index - len(bin_value)
        bin_value = bin_value.rjust(needed_pad, '0')
    bin_value = bin_value.zfill(36)
    return bin_value, original_bin_length


def apply_mask(bin_value, bitmask):
    masked_bin_value = list(bin_value)
    for index, char in enumerate(bitmask):
        if char != 'X':
            masked_bin_value[index] = char
    return ''.join(masked_bin_value)


def mask_decode(bin_value, bitmask, mem_value):
    masked_bin_value = list(bin_value)
    changed_value_indeces = []
    for index, char in enumerate(bitmask):
        if bitmask[index] != '0':
            masked_bin_value[index] = char
            if char == 'X':
                changed_value_indeces.append(index)
    combinations = [x for x in itertools.product('01', repeat=len(changed_value_indeces))]
    for combi in combinations:
        mem_temp = masked_bin_value.copy()
        for index, value in enumerate(combi):
            mem_temp[changed_value_indeces[index]] = value
        mem[int(''.join(mem_temp), base=2)] = mem_value

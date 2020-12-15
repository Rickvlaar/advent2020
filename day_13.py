import util
import math

raw_schedule = util.parse_file_as_list('input_files/day_13.txt')


def check_schedule():
    departure_time = int(raw_schedule[0])
    bus_ids = [int(bus_id) for bus_id in raw_schedule[1].split(',') if bus_id != 'x']
    bus_wait_times = {}
    for bus_id in bus_ids:
        wait_time = bus_id - (departure_time % bus_id)
        bus_wait_times[bus_id] = wait_time
    return bus_wait_times


def diff_approach():
    bus_id_time_offset_dict = {int(bus_id): time_offset for time_offset, bus_id in enumerate(raw_schedule[1].split(',')) if bus_id != 'x'}
    bus_ids = [bus_id for bus_id in bus_id_time_offset_dict.keys()]
    bus_ids.sort()
    common_denom = bus_ids[0]
    first_occ = 0
    for index, bus_id in enumerate(bus_ids):
        if index > 0:
            this_buss_offset = bus_id_time_offset_dict.get(bus_id)
            offset_diff = this_buss_offset - bus_id_time_offset_dict.get(bus_ids[index - 1])
            offset = first_occ + offset_diff
            common_denom, first_occ = find_common_denom_start(common_denom, bus_id, offset)
    return common_denom, first_occ - this_buss_offset


def find_common_denom_start(num, num_new, offset):
    x = 1
    while True:
        if 0 == ((x * num) + offset) % num_new:
            first_occ = (x * num) + offset
            common_denom = math.lcm(num, num_new)
            return common_denom, first_occ
        x += 1

import util
import numpy

seat_file = 'input_files/day_11.txt'
seat_list = util.parse_file_as_list(seat_file)


def seat_the_people(seat_list=seat_list, max_occupied=5, distance=int(10e12)):
    seat_map = {(x, y): char for y, line in enumerate(seat_list) for x, char in enumerate(line)}
    the_matrix = numpy.array([list(line) for line in seat_list])
    still_movin_around = True
    while still_movin_around:
        still_movin_around = False
        locations_to_change = {}
        for location, char in seat_map.items():
            if char != '.':
                coords_to_check = check_matrix(the_matrix, location[0], location[1], distance)
                if coords_to_check.count('#') >= max_occupied and char == '#':
                    locations_to_change[location] = 'L'
                elif coords_to_check.count('#') == 0 and char == 'L':
                    locations_to_change[location] = '#'
        if len(locations_to_change) > 0:
            still_movin_around = True
            for loc, new_value in locations_to_change.items():
                seat_map[loc] = new_value
                the_matrix[loc[1]][loc[0]] = new_value
    return sum([1 for hekje in seat_map.values() if hekje == '#'])


def check_matrix(the_matrix, x, y, distance=int(10e12)):
    coords_to_check = []
    coords_to_check = list_checker(x, the_matrix[y], coords_to_check, distance)  # check the row
    coords_to_check = list_checker(x, numpy.flip(the_matrix[y]), coords_to_check, distance, True)  # reverse to look the other way
    coords_to_check = list_checker(y, the_matrix[:, x], coords_to_check, distance)  # check the column
    coords_to_check = list_checker(y, numpy.flip(the_matrix[:, x]), coords_to_check,  distance, True)  # reverse

    min_value = x if y > x else y
    coords_to_check = list_checker(min_value, the_matrix.diagonal(x - y), coords_to_check, distance)  # check diagonal
    coords_to_check = list_checker(min_value, numpy.flip(the_matrix.diagonal(x - y)), coords_to_check, distance, True)  # reverse diagonal

    diag_x = len(the_matrix[0]) - (x + 1)  # for selecting the correct diagonal
    min_value = len(the_matrix[0]) - (x + 1) if y > (len(the_matrix[0]) - (x + 1)) else y
    coords_to_check = list_checker(min_value, numpy.fliplr(the_matrix).diagonal(diag_x - y), coords_to_check, distance)  # other diagonal
    coords_to_check = list_checker(min_value, numpy.flip(numpy.fliplr(the_matrix).diagonal(diag_x - y)), coords_to_check, distance, True)  # other diagonal
    return coords_to_check


def list_checker(min_value, list_to_check, coords_to_check, distance=int(10e12), reverse=False):
    if reverse:
        min_value = len(list_to_check) - (min_value + 1)
    for pos, char in enumerate(list_to_check):
        if min_value + distance >= pos > min_value and (char == '#' or char == 'L'):
            coords_to_check.append(char)
            break
    return coords_to_check

import util

seats_file = 'input_files/day_5.txt'


def parse_seat_ids():
    seats_lists = [line.translate(str.maketrans({'F': '0', 'L': '0', 'B': '1', 'R': '1'})) for line in util.parse_file_as_list(seats_file)]
    seat_ids = [int(x, 2) for x in seats_lists]
    my_seat = set(range(80, int('1' * 10, 2))) - set(seat_ids)
    print(max(seat_ids))
    print(min(my_seat))


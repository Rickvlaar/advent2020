import util

test_file = 'input_files/day_24_test.txt'
real_file = 'input_files/day_24.txt'


class Grid:
    def __init__(self):
        self.current_hexagon = self.Hexagon((0, 0))
        self.placed_hexagons = {self.current_hexagon.coordinates: self.current_hexagon}
        self.place_neighbours(self.current_hexagon)

    def parse_direction_string(self, direction_string):
        while len(direction_string) > 0:
            first_letter = direction_string[0]
            if first_letter == 'e' or first_letter == 'w':
                direction = direction_string[0]
                self.move_to_neighbour(direction)
                direction_string = direction_string[1:]
            elif first_letter == 's' or first_letter == 'n':
                direction = direction_string[0:2]
                self.move_to_neighbour(direction)
                direction_string = direction_string[2:]
        else:
            self.current_hexagon.color = 'black' if self.current_hexagon.color == 'white' else 'white'

    def move_to_neighbour(self, direction):
        new_coords = list(self.current_hexagon.coordinates)
        if direction == 'e':
            new_coords[0] += 2
        if direction == 'se':
            new_coords[0] += 1
            new_coords[1] -= 1
        if direction == 'ne':
            new_coords[0] += 1
            new_coords[1] += 1
        if direction == 'w':
            new_coords[0] -= 2
        if direction == 'sw':
            new_coords[0] -= 1
            new_coords[1] -= 1
        if direction == 'nw':
            new_coords[0] -= 1
            new_coords[1] += 1
        new_coords = tuple(new_coords)
        if new_coords in self.placed_hexagons:
            self.current_hexagon = self.placed_hexagons.get(new_coords)
            self.place_neighbours(self.current_hexagon)
        else:
            neighbour = self.Hexagon(new_coords)
            self.place_neighbours(neighbour)
            self.current_hexagon = neighbour
            self.placed_hexagons[new_coords] = self.current_hexagon

    def goto_start(self):
        self.current_hexagon = self.placed_hexagons.get((0, 0))

    def place_neighbours(self, neighbour):
        all_neighbour_coords = []
        center_coords = list(neighbour.coordinates)

        e = center_coords.copy()
        e[0] += 2
        all_neighbour_coords.append(tuple(e))

        se = center_coords.copy()
        se[0] += 1
        se[1] -= 1
        all_neighbour_coords.append(tuple(se))

        ne = center_coords.copy()
        ne[0] += 1
        ne[1] += 1
        all_neighbour_coords.append(tuple(ne))

        w = center_coords.copy()
        w[0] -= 2
        all_neighbour_coords.append(tuple(w))

        sw = center_coords.copy()
        sw[0] -= 1
        sw[1] -= 1
        all_neighbour_coords.append(tuple(sw))

        nw = center_coords.copy()
        nw[0] -= 1
        nw[1] += 1
        all_neighbour_coords.append(tuple(nw))

        for coord in all_neighbour_coords:
            if coord not in self.placed_hexagons:
                new_hexagon = self.Hexagon(coord)
                self.placed_hexagons[coord] = new_hexagon
                neighbour.neighbours.add(new_hexagon)
            else:
                existing_hexagon = self.placed_hexagons.get(coord)
                neighbour.neighbours.add(existing_hexagon)

    def daily_flip(self):
        current_hexagons = list(self.placed_hexagons.values())
        for hexagon in current_hexagons:
            self.place_neighbours(hexagon)

        for hexagon in self.placed_hexagons.values():
            hexagon.get_neighbour_colors()

        for hexagon in self.placed_hexagons.values():
            if hexagon.color == 'black' and (hexagon.black_neighbour_count == 0 or hexagon.black_neighbour_count > 2):
                hexagon.color = 'white'
            if hexagon.color == 'white' and hexagon.black_neighbour_count == 2:
                hexagon.color = 'black'

    def print_hexagons(self):
        whites = 0
        blacks = 0
        for hexagon in self.placed_hexagons.values():
            if hexagon.color == 'white':
                whites += 1
            elif hexagon.color == 'black':
                blacks += 1
        print('whites ' + str(whites) + '\n' + 'blacks ' + str(blacks))

    class Hexagon:
        def __init__(self, coordinates):
            self.e = None
            self.se = None
            self.sw = None
            self.w = None
            self.nw = None
            self.ne = None
            self.neighbours = set()
            self.color = 'white'
            self.white_neighbour_count = 0
            self.black_neighbour_count = 0
            self.coordinates = coordinates

        def __repr__(self):
            return self.color

        def get_neighbour_colors(self):
            self.white_neighbour_count = 0
            self.black_neighbour_count = 0
            for hexagon in self.neighbours:
                if hexagon.color == 'white':
                    self.white_neighbour_count += 1
                elif hexagon.color == 'black':
                    self.black_neighbour_count += 1


def flip_it():
    string_list = util.parse_file_as_list(real_file)

    the_grid = Grid()
    for direction_string in string_list:
        the_grid.parse_direction_string(direction_string)
        the_grid.goto_start()
    the_grid.print_hexagons()

    for x in range(100):
        the_grid.daily_flip()
    the_grid.print_hexagons()


flip_it()

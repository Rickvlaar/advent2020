all_hexagons = []


class Hexagon:
    def __init__(self):
        self.e = None
        self.se = None
        self.sw = None
        self.w = None
        self.nw = None
        self.ne = None
        self.color = 'white'
        self.direction_dict = {
                'e': self.e,
                'se': self.se,
                'sw': self.sw,
                'w': self.w,
                'nw': self.nw,
                'ne': self.ne
        }

    def parse_direction_string(self, direction_string):
        if len(direction_string) > 0:
            first_letter = direction_string[0]
            direction = ''
            if first_letter == 'e' or first_letter == 'w':
                direction = direction_string[0]
                self.move_to_neighbour(direction, direction_string[1:])
            elif first_letter == 's' or first_letter == 'n':
                direction = direction_string[0:2]
                self.move_to_neighbour(direction, direction_string[2:])
        else:
            self.color = 'black' if self.color == 'white' else 'white'

    def move_to_neighbour(self, direction, direction_string):
        neighbour = self.__dict__.get(direction)
        if neighbour is None:
            neighbour = Hexagon()
            self.__dict__[direction] = neighbour
            all_hexagons.append(neighbour)
        neighbour.parse_direction_string(direction_string)


def flip_it(direction_string):
    global all_hexagons
    first_tile = Hexagon()
    all_hexagons.append(first_tile)
    first_tile.parse_direction_string('nwwswee')


flip_it('nwwswee')

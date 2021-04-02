import numpy as np
import math
import re

test_file = 'input_files/day_20_test.txt'
image_file = 'input_files/day_20.txt'
monster_file = 'input_files/day_20_monster.txt'
np.set_printoptions(threshold=np.inf, linewidth=np.inf)


def recombine_image():
    tile_list = [tile.splitlines() for tile in open(file=image_file).read().split('\n\n')]

    # Create dictionary of tile_id to tile
    temp_dict = {tile[0][5:9]: np.array([list(line) for line in tile[1:]]) for tile in tile_list}

    tile_dict = {tile_id: Tile(tile_id, tile) for tile_id, tile in temp_dict.items()}

    side_length = int(math.sqrt(len(temp_dict.keys())))
    image = np.empty((side_length, side_length), dtype='object')

    corners = list()
    for tile in tile_dict.values():
        tile.get_matching_edge_tiles(tile_dict.values())
        if len(tile.neighbouring_tiles) == 2:
            corners.append(tile)
            tile.corner = True

    start_tile = corners[0]
    image[0][0] = start_tile

    # Start with top-left corner, mutate tile to work
    start_tile.get_neighbour_direction()
    while True:
        if start_tile.right_match and start_tile.bottom_match:
            break
        start_tile.rotate_90()
        start_tile.get_neighbour_direction()

    # Fill the image
    for y, y_line in enumerate(image):
        for x, tile in enumerate(y_line):
            # First of line, match to top
            if x == 0 and y > 0:
                top_neighbour_tile = image[y - 1][x]
                top_neighbour_tile.bottom_match.orient_tile_top(top_neighbour_tile)
                top_neighbour_tile.bottom_match.get_neighbour_direction()
                image[y][x] = top_neighbour_tile.bottom_match
            elif x > 0:
                left_neighbour_tile = image[y][x - 1]
                left_neighbour_tile.right_match.orient_tile_left(left_neighbour_tile)
                left_neighbour_tile.right_match.get_neighbour_direction()
                image[y][x] = left_neighbour_tile.right_match

    print(image)
    monochrome_image = print_image(image)
    find_monsters(monochrome_image)


def find_monsters(image):
    # Use regexp to find monster like pattern
    image = image
    image_array = np.array([list(line) for line in image.split('\n') if line != ''])

    # image_array = np.flipud(image_array)
    monsters_found = 0
    for x in range(4):
        for line_no, line in enumerate(image_array):
            suspected_monsters = re.finditer('#.{4}##.{4}##.{4}###', ''.join(line))
            if suspected_monsters:
                print('susss')
                for suspected_monster in suspected_monsters:
                    try:
                        line_above = ''.join(image_array[line_no - 1])
                        line_below = ''.join(image_array[line_no + 1])

                        start_point = suspected_monster.start()
                        end_point = suspected_monster.end()

                        monster_head = re.search('.{18}#', line_above[start_point: end_point])
                        monster_body = re.search('.#.{2}#.{2}#.{2}#.{2}#.{2}#', line_below[start_point: end_point])
                        if monster_body and monster_head:
                            print('found_one')
                            monsters_found += 1
                    except IndexError:
                        pass
        image_array = np.rot90(image_array, k=1)
    print(monsters_found)
    print(image.count('#'))
    print('rough waters:')
    print(image.count('#') - monsters_found * 15)

class Tile:
    def __init__(self, tile_id, tile):
        self.tile_id = tile_id
        self.tile = tile
        self.top = self.tile[0]
        self.right = self.tile[:, -1]
        self.bottom = self.tile[-1]
        self.left = self.tile[:, 0]
        self.edge_possibilities = self.get_edge_possibilities()
        self.neighbouring_tiles = set()
        self.corner = False
        self.image_coords = None
        self.tile_dict = None
        self.to_be_placed = True
        self.top_match = None
        self.right_match = None
        self.bottom_match = None
        self.left_match = None

    def get_edge_possibilities(self):
        return {self.top.tobytes(),
                self.right.tobytes(),
                self.bottom.tobytes(),
                self.left.tobytes(),
                np.flip(self.top).tobytes(),
                np.flip(self.right).tobytes(),
                np.flip(self.bottom).tobytes(),
                np.flip(self.left).tobytes()}

    def get_edges(self):
        return {self.top.tobytes(), self.right.tobytes(), self.bottom.tobytes(), self.left.tobytes()}

    def get_edges_dict(self):
        return {'top'   : self.top.tobytes(),
                'right' : self.right.tobytes(),
                'bottom': self.bottom.tobytes(),
                'left'  : self.left.tobytes()}

    def get_matches_dict(self):
        return {'top'   : self.top_match,
                'right' : self.right_match,
                'bottom': self.bottom_match,
                'left'  : self.left_match}

    def get_matching_edge_tiles(self, tiles_to_compare):
        for compare_tile in tiles_to_compare:
            if compare_tile.tile_id != self.tile_id and compare_tile.tile_id not in self.neighbouring_tiles:
                if not self.edge_possibilities.isdisjoint(compare_tile.edge_possibilities):
                    self.neighbouring_tiles.add(compare_tile)

    def get_neighbour_direction(self):
        self.top_match = None
        self.right_match = None
        self.bottom_match = None
        self.left_match = None

        for neighbour in self.neighbouring_tiles:
            for direction, edge in self.get_edges_dict().items():
                if direction == 'top' and edge in neighbour.get_edge_possibilities():
                    self.top_match = neighbour
                elif direction == 'right' and edge in neighbour.get_edge_possibilities():
                    self.right_match = neighbour
                elif direction == 'bottom' and edge in neighbour.get_edge_possibilities():
                    self.bottom_match = neighbour
                elif direction == 'left' and edge in neighbour.get_edge_possibilities():
                    self.left_match = neighbour

    def orient_tile_left(self, left_neighbour):
        count = 0
        while True:
            if left_neighbour.right.tobytes() == self.left.tobytes():
                break
            self.rotate_90()
            if count % 5 == 0:
                self.flip_tile()
            elif count > 10:
                break
            count += 1

    def orient_tile_top(self, top_neighbour):
        count = 0
        while True:
            if top_neighbour.bottom.tobytes() == self.top.tobytes():
                break
            self.rotate_90()
            if count % 3 == 0:
                self.flip_tile()
            count += 1

    def flip_tile(self):
        self.tile = np.flipud(self.tile)
        self.update_edges()

    def rotate_90(self):
        self.tile = np.rot90(self.tile, k=1)
        self.update_edges()

    def update_edges(self):
        self.top = self.tile[0]
        self.right = self.tile[:, -1]
        self.bottom = self.tile[-1]
        self.left = self.tile[:, 0]

    def __repr__(self):
        return self.tile_id


def print_image(tile_matrix):
    image = ''
    for y_ind, y_lists in enumerate(tile_matrix):
        if y_lists.any():
            y_string = ''
            for line_ind in range(1, 9):
                image_line_str = ''.join([str(x_lists.tile[line_ind]).replace('[',
                                                                              '').replace(
                        ']', '').replace('\'', '').replace(' ', '')[1:9] for x_lists in y_lists if x_lists])
                y_string = y_string + image_line_str + '\n'
            image = image + y_string
    print(image)
    return image


recombine_image()

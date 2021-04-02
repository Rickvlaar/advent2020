import numpy as np
import math
import itertools

test_file = 'input_files/day_20_test.txt'
image_file = 'input_files/day_20.txt'
np.set_printoptions(threshold=np.inf, linewidth=np.inf)


def recombine_image():
    tile_list = [tile.splitlines() for tile in open(file=test_file).read().split('\n\n')]
    temp_dict = {tile[0][5:9]: np.array([list(line) for line in tile[1:]]) for tile in tile_list}

    tile_dict = {tile_id: Tile(tile_id, tile) for tile_id, tile in temp_dict.items()}

    side_length = int(math.sqrt(len(temp_dict.keys())))
    image = np.empty((side_length * 2 + side_length, side_length * 2 + side_length), dtype='object')

    for tile in tile_dict.values():
        tile.tile_dict = tile_dict

    # Place an initial tile to start working with
    for tile in tile_dict.values():
        tile.get_matching_edge_tiles(tile_dict.values())
        if len(tile.neighbouring_tiles) == 4:
            image[side_length, side_length] = tile
            tile.image_coords = (side_length, side_length)
            tile.position_neighbours()
            break

    # Flip all remaining tiles and restart the flow

    for x in range(100):
        for tile in tile_dict.values():
            if tile.to_be_placed:
                print(tile)
                tile.flip_tile()
                tile.get_matching_edge_tiles(tile_dict.values())

        for tile in tile_dict.values():
            if len(tile.neighbouring_tiles) > 1 and tile.to_be_placed:
                tile.position_neighbours()
                break

    for tile in tile_dict.values():
        if tile.image_coords:
            image[tile.image_coords] = tile

    print(image)
    print_image(image)
    return tile_dict


class Tile:
    def __init__(self, tile_id, tile):
        self.tile_id = tile_id
        self.tile = tile
        self.top = self.tile[0]
        self.right = self.tile[:, -1]
        self.bottom = self.tile[-1]
        self.left = self.tile[:, 0]
        self.top_match = None
        self.right_match = None
        self.bottom_match = None
        self.left_match = None
        self.neighbouring_tiles = set()
        self.image_coords = None
        self.tile_dict = None
        self.to_be_placed = True

    def get_edges(self):
        return {self.top.tobytes(), self.right.tobytes(), self.bottom.tobytes(), self.left.tobytes()}

    def get_edges_dict(self):
        return {'top': self.top.tobytes(), 'right': self.right.tobytes(), 'bottom': self.bottom.tobytes(), 'left': self.left.tobytes()}

    def get_matches_dict(self):
        return {'top': self.top_match, 'right': self.right_match, 'bottom': self.bottom_match, 'left': self.left_match}

    def get_matching_edge_tiles(self, tiles_to_compare):
        for compare_tile in tiles_to_compare:
            if compare_tile.tile_id != self.tile_id and compare_tile.tile_id not in self.neighbouring_tiles:
                if not self.get_edges().isdisjoint(compare_tile.get_edges()):
                    self.neighbouring_tiles.add(compare_tile)

    def position_neighbours(self):
        self.to_be_placed = False
        self.get_matching_edge_tiles(self.tile_dict.values())
        if not self.image_coords:
            self.determine_coordinates()
        if self.image_coords:
            for tile in self.neighbouring_tiles:
                if tile.to_be_placed:
                    self.get_match_orientation(tile)
            for neighbour in self.neighbouring_tiles:
                if neighbour.to_be_placed and neighbour.image_coords:
                    neighbour.position_neighbours()

    def get_match_orientation(self, match_tile):
        for direction, edge in self.get_edges_dict().items():
            for match_dir, match_edge in match_tile.get_edges_dict().items():
                if edge == match_edge:
                    if direction == 'top':
                        self.top_match = match_tile.orientate_to_neighbour(match_dir, direction)
                        match_tile.bottom_match = self
                        match_tile.image_coords = self.image_coords[0] - 1, self.image_coords[1]
                    elif direction == 'right':
                        self.right_match = match_tile.orientate_to_neighbour(match_dir, direction)
                        match_tile.left_match = self
                        match_tile.image_coords = self.image_coords[0], self.image_coords[1] + 1
                    elif direction == 'bottom':
                        self.bottom_match = match_tile.orientate_to_neighbour(match_dir, direction)
                        match_tile.top_match = self
                        match_tile.image_coords = self.image_coords[0] + 1, self.image_coords[1]
                    elif direction == 'left':
                        self.left_match = match_tile.orientate_to_neighbour(match_dir, direction)
                        match_tile.right_match = self
                        match_tile.image_coords = self.image_coords[0], self.image_coords[1] - 1
                    # if self in match_tile.neighbouring_tiles:
                    #     match_tile.neighbouring_tiles.remove(self)

    def orientate_to_neighbour(self, edge_orientation, position_to_neighbour):
        if position_to_neighbour == 'top':
            if edge_orientation == 'top':
                self.tile = np.flipud(self.tile)
            if edge_orientation == 'right':
                self.tile = np.rot90(self.tile, k=3)
            if edge_orientation == 'left':
                self.tile = np.rot90(self.tile, k=1)
        elif position_to_neighbour == 'right':
            if edge_orientation == 'top':
                self.tile = np.rot90(self.tile, k=1)
            if edge_orientation == 'right':
                self.tile = np.fliplr(self.tile)
            if edge_orientation == 'bottom':
                self.tile = np.rot90(self.tile, k=3)
        elif position_to_neighbour == 'bottom':
            if edge_orientation == 'bottom':
                self.tile = np.flipud(self.tile)
            if edge_orientation == 'left':
                self.tile = np.rot90(self.tile, k=3)
            if edge_orientation == 'right':
                self.tile = np.rot90(self.tile, k=1)
        elif position_to_neighbour == 'left':
            if edge_orientation == 'top':
                self.tile = np.rot90(self.tile, k=3)
            if edge_orientation == 'left':
                self.tile = np.fliplr(self.tile)
            if edge_orientation == 'bottom':
                self.tile = np.rot90(self.tile, k=1)
        self.update_edges()
        return self

    def determine_coordinates(self):
        for match in self.neighbouring_tiles:
            if match is not None and match.image_coords:
                if self.top.tobytes() in match.get_edges():
                    self.image_coords = match.image_coords[0] - 1, match.image_coords[1]
                    match.get_match_orientation(self)
                elif self.right.tobytes() in match.get_edges():
                    self.image_coords = match.image_coords[0], match.image_coords[1] + 1
                    match.get_match_orientation(self)
                elif self.bottom.tobytes() in match.get_edges():
                    self.image_coords = match.image_coords[0] + 1, match.image_coords[1]
                    match.get_match_orientation(self)
                elif self.left.tobytes() in match.get_edges():
                    self.image_coords = match.image_coords[0], match.image_coords[1] - 1
                    match.get_match_orientation(self)
                return

    def flip_tile(self):
        self.tile = np.flipud(self.tile)
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
            for line_ind in range(10):
                image_line_str = ''.join([str(x_lists.tile[line_ind]) for x_lists in y_lists if x_lists]).replace('[', ' ').replace(']','  ')
                y_string = y_string + image_line_str + '\n'
            image = image + y_string + '\n'
    print(image)


recombine_image()

import numpy as np
import math
import itertools

test_file = 'input_files/day_20_test.txt'
image_file = 'input_files/day_20.txt'

class TileMatch:
    def __init__(self, top_match=None, right_match=None, bottom_match=None, left_match=None):
        self.top_match = top_match
        self.right_match = right_match
        self.bottom_match = bottom_match
        self.left_match = left_match

    def match_count(self):
        return sum([1 for value in self.__dict__.values() if value])

    def get_matches_dict(self):
        return {key: value for key, value in self.__dict__.items() if value}


def recombine_image():
    tile_list = [tile.splitlines() for tile in open(file=test_file).read().split('\n\n')]
    tile_dict = {tile[0][5:9]: np.array([list(line) for line in tile[1:]]) for tile in tile_list}

    # could be useful for efficiency
    for tile_id, tile in tile_dict.items():
        tile = np.where(tile == '#', 1, 0)
        tile_dict[tile_id] = tile

    side_length = int(math.sqrt(len(tile_dict.keys())))
    image = np.empty((side_length * 2 + 1, side_length * 2 + 1), dtype='object')
    match_tiles(image, tile_dict, side_length)

    # print(create_image(tile_matrix))
    return


def match_tiles(image, tile_dict, side_length):
    matches_dict = get_edge_tiles(tile_dict)

    starting_tile_id = None
    positioned_tiles = set()
    placeable_tiles = set()

    for tile_id, tile_match in matches_dict.items():
        if tile_match.match_count() > 0:
            placeable_tiles.add(tile_id)
            starting_tile_id = tile_id

    tile_matches = matches_dict.get(starting_tile_id)
    positioned_tiles.add(starting_tile_id)
    image[side_length, side_length] = starting_tile_id

    coords = np.where(image == starting_tile_id)
    x = coords[1][0]
    y = coords[0][0]

    for orientation, match in tile_matches.get_matches_dict().items():
        matched_tile_id, edge = match
        if matched_tile_id not in positioned_tiles:
            print(matched_tile_id)
            flip_n_rotate_match(tile_dict, matched_tile_id, orientation, edge, image, positioned_tiles, x, y)

    still_matching = True
    while still_matching:
        still_matching = positioned_tiles != placeable_tiles
        matches_dict = get_edge_tiles(tile_dict)
        for tile_id, tile_match in matches_dict.items():
            if tile_match.match_count() > 0:
                starting_tile_id = tile_id
                if starting_tile_id in image:
                    tile_matches = matches_dict.get(starting_tile_id)
                    coords = np.where(image == starting_tile_id)
                    x = coords[1][0]
                    y = coords[0][0]
                    print('tile with matches: ' + starting_tile_id)
                    for orientation, match in tile_matches.get_matches_dict().items():
                        matched_tile_id, edge = match
                        if matched_tile_id not in positioned_tiles:
                            print('placing tile: ' + matched_tile_id)
                            print(orientation)
                            print(match)
                            flip_n_rotate_match(tile_dict, matched_tile_id, orientation, edge, image, positioned_tiles, x, y)
    print(image)


def flip_n_rotate_match(tile_dict, tile_id, orientation, edge, image, positioned_tiles, x, y):
    print(image)
    print(create_image(create_tile_matrix(tile_dict, image)))

    if orientation == 'top_match':
        image[y - 1, x] = tile_id
        positioned_tiles.add(tile_id)

        if edge == 'top':
            tile_dict[tile_id] = np.flipud(tile_dict.get(tile_id))

        if edge == 'right':
            tile_dict[tile_id] = np.rot90(tile_dict.get(tile_id), k=3)

        if edge == 'left':
            tile_dict[tile_id] = np.rot90(tile_dict.get(tile_id), k=1)

    if orientation == 'right_match':
        image[y, x + 1] = tile_id
        positioned_tiles.add(tile_id)
        print(edge)

        if edge == 'top':
            tile_dict[tile_id] = np.rot90(tile_dict.get(tile_id), k=1)

        if edge == 'right':
            tile_dict[tile_id] = np.fliplr(tile_dict.get(tile_id))

        if edge == 'bottom':
            tile_dict[tile_id] = np.rot90(tile_dict.get(tile_id), k=3)

        if edge == 'left':
            positioned_tiles.add(tile_id)

    if orientation == 'bottom_match':
        image[y + 1, x] = tile_id
        positioned_tiles.add(tile_id)

        if edge == 'right':
            tile_dict[tile_id] = np.rot90(tile_dict.get(tile_id), k=1)

        if edge == 'bottom':
            tile_dict[tile_id] = np.flipud(tile_dict.get(tile_id))

        if edge == 'left':
            tile_dict[tile_id] = np.rot90(tile_dict.get(tile_id), k=3)

    if orientation == 'left_match':
        image[y, x - 1] = tile_id
        positioned_tiles.add(tile_id)

        if edge == 'top':
            tile_dict[tile_id] = np.rot90(tile_dict.get(tile_id), k=3)

        if edge == 'bottom':
            tile_dict[tile_id] = np.rot90(tile_dict.get(tile_id), k=1)

        if edge == 'left':
            tile_dict[tile_id] = np.fliplr(tile_dict.get(tile_id))


def get_edge_tiles(tile_dict):
    tile_match_dict = {}

    for tile_id, tile in tile_dict.items():
        top = tile[0]
        bottom = tile[-1]
        left = tile[:, 0]
        right = tile[:, -1]

        match_results = TileMatch(
                top_match=match_edge(top, tile_id, tile_dict),
                right_match=match_edge(right, tile_id, tile_dict),
                bottom_match=match_edge(bottom, tile_id, tile_dict),
                left_match=match_edge(left, tile_id, tile_dict)
        )

        tile_match_dict[tile_id] = match_results

    return tile_match_dict


def match_edge(edge, edge_tile_id, tile_dict):
    for tile_id, tile in tile_dict.items():
        top = tile[0]
        bottom = tile[-1]
        left = tile[:, 0]
        right = tile[:, -1]
        if edge_tile_id != tile_id:
            compare = edge == top
            if compare.all():
                return tile_id, 'top'
            compare = edge == bottom
            if compare.all():
                return tile_id, 'bottom'
            compare = edge == left
            if compare.all():
                return tile_id, 'left'
            compare = edge == right
            if compare.all():
                return tile_id, 'right'
    return False


def create_tile_matrix(tile_dict, image):
    side_length = int(math.sqrt(len(tile_dict.keys())))
    tiles = [value for value in tile_dict.values()]
    two_d_tiles = []
    image_length = len(image)

    for index, y in enumerate(image.tolist()):
        two_d_tiles.append([])
        for x in y:
            if x:
                two_d_tiles[index].append(tile_dict.get(x))
    return two_d_tiles


def create_image(tile_matrix):
    image = ''
    for y_ind, y_lists in enumerate(tile_matrix):
        if y_lists:
            y_string = ''
            for line_ind in range(10):
                image_line_str = ''.join([str(x_lists[line_ind]) for x_lists in y_lists]).replace('[', ' ').replace(']',
                                                                                                                    '  ')
                y_string = y_string + image_line_str + '\n'
            image = image + y_string + '\n'
    return image

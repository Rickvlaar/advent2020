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

    def get_neighbour_ids(self):
        return set([value[0] for value in self.__dict__.values() if value])


def recombine_image():
    tile_list = [tile.splitlines() for tile in open(file=test_file).read().split('\n\n')]
    tile_dict = {tile[0][5:9]: np.array([list(line) for line in tile[1:]]) for tile in tile_list}

    # could be useful for efficiency
    # for tile_id, tile in tile_dict.items():
    #     tile = np.where(tile == '#', 1, 0)
    #     tile_dict[tile_id] = tile

    side_length = int(math.sqrt(len(tile_dict.keys())))
    image = np.empty((side_length * 2 + side_length, side_length * 2 + side_length), dtype='object')
    # match_tiles(image, tile_dict, side_length)
    match_tile_dict(tile_dict, image)

    return


def match_tiles(image, tile_dict, side_length):
    matches_dict = get_edge_tiles(tile_dict)

    starting_tile_id = None
    positioned_tiles = set()
    placeable_tiles = set()

    for tile_id, tile_match in matches_dict.items():
        if tile_match.match_count() > 0:
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
            flip_n_rotate_match(tile_dict, matched_tile_id, orientation, edge, image, positioned_tiles, x, y)

    still_matching = True
    while still_matching:
        still_matching = positioned_tiles != placeable_tiles
        matches_dict = get_edge_tiles(tile_dict)
        placeable_tiles.clear()
        for tile_id, tile_match in matches_dict.items():
            if tile_match.match_count() > 1:
                placeable_tiles.add(tile_id)
                tile_placed = False
                starting_tile_id = tile_id
                if starting_tile_id in image:
                    tile_matches = matches_dict.get(starting_tile_id)
                    coords = np.where(image == starting_tile_id)
                    x = coords[1][0]
                    y = coords[0][0]
                    # print('tile with matches: ' + starting_tile_id)
                    # print(tile_matches.get_matches_dict())
                    for orientation, match in tile_matches.get_matches_dict().items():
                        matched_tile_id, edge = match
                        if matched_tile_id not in positioned_tiles:
                            # print('placing tile: ' + matched_tile_id)
                            # print(orientation)
                            # print(match)
                            tile_placed = flip_n_rotate_match(tile_dict, matched_tile_id, orientation, edge, image,
                                                              positioned_tiles, x, y)
                    if tile_placed:
                        break
            else:
                tile_dict[tile_id] = np.fliplr(tile_dict.get(tile_id))
    print(image)
    print(create_image(create_tile_matrix(tile_dict, image)))


def flip_n_rotate_match(tile_dict, tile_id, orientation, edge, image, positioned_tiles, x, y):
    # print(image)
    # print(create_image(create_tile_matrix(tile_dict, image)))

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

        if edge == 'top':
            tile_dict[tile_id] = np.rot90(tile_dict.get(tile_id), k=1)

        if edge == 'right':
            tile_dict[tile_id] = np.fliplr(tile_dict.get(tile_id))

        if edge == 'bottom':
            tile_dict[tile_id] = np.rot90(tile_dict.get(tile_id), k=3)

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

    return True


def match_tile_dict(tile_dict, image):
    matches_dict = get_edge_tiles(tile_dict)
    for parent_tile_id, tile in matches_dict.items():

        all_neighbour_matches = []
        for tile_id in tile.get_neighbour_ids():
            all_neighbour_matches.append(get_neighbours(tile_id, tile_dict))

        #     create sets of two neighbours to see what tile can be placed next
        for neighbour_pair in itertools.combinations(tile.get_neighbour_ids(), 2):
            for tile_id, available_tile in matches_dict.items():
                if set(neighbour_pair).issubset(available_tile.get_neighbour_ids()):
                    place_and_orient_tile(tile_id, available_tile, neighbour_pair, image)


def place_and_orient_tile(tile_id, available_tile, neighbour_pair, parent_tile_id, image):
    parent_coords = np.where(image == parent_tile_id)
    for id in neighbour_pair:
        coords = np.where(image == id)
        if parent_coords[1][0] != coords[1][0]:
            new_tile_x = coords[1][0]
        if parent_coords[0][0] != coords[0][0]:
            new_tile_y = coords[1][0]

    pass


def get_neighbours(tile_id, tile_dict):
    tile = tile_dict.get(tile_id)
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

    return match_results


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
    two_d_tiles = []

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

import numpy as np
import math

test_file = 'input_files/day_20_test.txt'
image_file = 'input_files/day_20.txt'


def recombine_image():
    tile_list = [tile.splitlines() for tile in open(file=image_file).read().split('\n\n')]
    tile_dict = {tile[0][5:9]: np.array([list(line) for line in tile[1:]]) for tile in tile_list}

    for tile_id, tile in tile_dict.items():
        tile = np.where(tile == '#', 1, 0)
        tile_dict[tile_id] = tile

    side_length = int(math.sqrt(len(tile_dict.keys())))
    image = np.array(np.zeros(shape=(side_length, side_length)))
    get_edge_tiles(tile_dict)

    return tile_dict


def get_edge_tiles(tile_dict):
    for tile_id, tile in tile_dict.items():
        top = tile[0]
        bottom = tile[-1]
        left = tile[:, 0]
        right = tile[:, -1]

        top_result = match_edge(top, tile_id, tile_dict)
        bottom_result = match_edge(bottom, tile_id, tile_dict)
        left_result = match_edge(left, tile_id, tile_dict)
        right_result = match_edge(right, tile_id, tile_dict)

        print(tile_id, top_result)
        print(tile_id, bottom_result)
        print(tile_id, left_result)
        print(tile_id, right_result)


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

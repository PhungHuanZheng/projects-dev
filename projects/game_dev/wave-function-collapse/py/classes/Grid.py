from __future__ import annotations

import os
import random
from copy import deepcopy
from itertools import chain
from PIL import Image

import numpy as np

from classes.helpers import Shape
from classes.Tile import Tile


class Grid: 
    def __init__(self, width: int, height: int, data_folder: os.PathLike, verbose: bool = True) -> None:
        # basic attribute init
        self.shape = Shape(width, height)
        self._verbose = verbose
        self._data_folder = data_folder

        # load images from data folder
        self._tile_shape: tuple[int, int, int] = None
        self._tile_imgs: list[np.ndarray] = []

        for i, filename in enumerate(os.listdir(data_folder), start=1):
            # read image into NDArray
            filepath = os.path.join(data_folder, filename)
            image_arr = np.array(Image.open(filepath)) / 255

            # validate image shapes
            if self._tile_shape is None:
                self._tile_shape = image_arr.shape

            elif self._tile_shape != image_arr.shape:
                raise ValueError(f'Image {filepath} has a shape ({image_arr.shape}) inconsistent with the template shape ({self._tile_shape}).')
            
            # track images
            self._tile_imgs.append(image_arr)

            if verbose:
                print(f'[{i}/{len(os.listdir(data_folder))}] [LOADED] "{filepath}"')

        # print debug stuff
        if verbose:
            print(f'\n{len(self._tile_imgs)} images loaded successfully from "{data_folder}"')
            print(f'Common image size: {self._tile_shape}')

        # init tiles and related data
        self._tiles = [[Tile(x, y, len(self._tile_imgs)) for x in range(self.shape.w)] for y in range(self.shape.h)]

    @property
    def flat_tiles(self) -> list[Tile]:
        return list(chain.from_iterable(self._tiles))

    def tile_at(self, x: int, y: int) -> Tile:
        return self._tiles[y][x]

    def force_collapse_random(self, count: int) -> None:
        for _ in range(count):
            # keep iterating in case land on an already collapsed tile
            while (True):
                # get random tile
                randx = random.randint(0, self.shape.w - 1)
                randy = random.randint(0, self.shape.h - 1)
                tile = self.tile_at(randx, randy)

                # if not already collapsed, collapse
                if not tile.is_collapsed:
                    tile.collapse()
                    break

    def generate_matches(self, threshold: float, sections: int = 1, depth: int = 1) -> list[list[list[int]]]:
        """
        Analyses image borders between every image and every other image and decides
        if they can be joined together based on the threshold passed used to compare
        border pixel differences. Generates a nested list where the first axis is the 
        image index, the second index is each direction as: `UP`, `RIGHT`, `DOWN`, `LEFT`
        and the third axis is which other images can be there for each main image for each
        direction. The lookup table is used in the `Grid.generate` method.

        Parameters
        ----------
        `threshold` : `float`
            How leniently to form possible neighbours between tiles. The threshold is compared
            against a value between 0 and 1, the mean pixel difference. If the difference is less
            than the threshold passed, the `other` image is considered a possible neighbour, where
            a threshold of 1.01 accepts all `other` images as possible neighbours.
        
        Returns
        -------
        `list[list[list[int]]]`
            Lookup table to be passed to `Grid.generate`.

        Examples
        --------
        Example of returned value
        >>> [[[0, 4], [0, 3], [0, 1], [0, 2]],
        ... [[0, 4], [1, 2, 4], [2, 3, 4], [1, 3, 4]],
        ... [[1, 2, 3], [0, 3], [2, 3, 4], [1, 3, 4]],
        ... [[1, 2, 3], [1, 2, 4], [2, 3, 4], [0, 2]],
        ... [[1, 2, 3], [1, 2, 4], [0, 1], [1, 3, 4]]]

        Example of `0` threshold returned value
        >>> [[[], [], [], []],
        ... [[], [], [], []],
        ... [[], [], [], []],
        ... [[], [], [], []],
        ... [[], [], [], []]]

        Example of `1` threshold returned value
        >>> [[[0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4]],
        ... [[0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4]],
        ... [[0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4]],
        ... [[0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4]],
        ... [[0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4]]]
        """

        # lookup table skeleton
        lookup: list[list[list[int]]] = [[[] for _ in range(4)] for _ in range(len(self._tile_imgs))]

        # iterate over images loaded from data folder
        for i, main in enumerate(self._tile_imgs):

            # iterate every other image again
            for j, other in enumerate(self._tile_imgs):

                # iterate over directions relative to main image arr
                # get borders between images based on direction joined
                for k, dir in enumerate(('TOP', 'RIGHT', 'DOWN', 'LEFT')):
                    # if other is on the top
                    if dir == 'TOP':
                        # get top of main and bottom of other
                        main_border = main[:depth, :, :].reshape(depth, main.shape[1], main.shape[2])
                        other_border = other[-depth:, :, :].reshape(depth, other.shape[1], other.shape[2])

                    # if other is on the right
                    elif dir == 'RIGHT':
                        # get top of main and bottom of other
                        main_border = main[:, -depth:, :].reshape(depth, main.shape[1], main.shape[2])
                        other_border = other[:, :depth, :].reshape(depth, other.shape[1], other.shape[2])

                    # if other is on the bottom
                    elif dir == 'DOWN':
                        # get top of main and bottom of other
                        main_border = main[-depth:, :, :].reshape(depth, main.shape[1], main.shape[2])
                        other_border = other[:depth, :, :].reshape(depth, other.shape[1], other.shape[2])

                    # if other is on the left
                    elif dir == 'LEFT':
                        # get top of main and bottom of other
                        main_border = main[:, :depth, :].reshape(depth, main.shape[1], main.shape[2])
                        other_border = other[:, -depth:, :].reshape(depth, other.shape[1], other.shape[2])

                    # get average pixel value difference between borders between sections
                    main_border = main_border.copy().flatten()
                    other_border = other_border.copy().flatten()

                    # split into sections
                    main_borders = np.split(main_border, sections)
                    other_borders = np.split(other_border, sections)

                    # get pixel diff
                    pixel_diff = 0
                    for g in range(sections):
                        pixel_diff += abs(np.mean(main_borders[g] - other_borders[g]))
                    pixel_diff /= 3

                    # compare diff against threshold
                    if abs(pixel_diff) < threshold:
                        lookup[i][k] += [j]
                        
        return lookup
    
    def update_tiles(self, lookup: list[list[list[int]]]) -> None:
        # iterate over tiles
        for y in range(self.shape.h):
            for x in range(self.shape.w):
                tile = self.tile_at(x, y)
                if not tile.is_collapsed:
                    continue

                # iterate over tile neighbours
                for i, relPos in enumerate(((0, -1), (1, 0), (0, 1), (-1, 0))):
                    # will fail if neighbour out of range
                    try:
                        # if neighbour is collapsed
                        neighbour = self.tile_at(tile.pos.x + relPos[0], tile.pos.y + relPos[1])
                        if not neighbour.is_collapsed:
                            new_states = set(lookup[tile.final_state][i]) & set(neighbour.possible_states)
                            neighbour.set_states(list(new_states))

                    except IndexError:
                        continue
    
    def generate(self, lookup: list[list[list[int]]], resize: tuple[int, int] = None, max_tries: int = 10, verbose: bool = False) -> Image:
        # iterate and keep trying
        for i in range(max_tries):
            grid = self.copy()

            # get list of uncollapsed tiles
            unsure_tiles = list(filter(lambda tile: not tile.is_collapsed, grid.flat_tiles))

            # if error thrown, failed generation
            try:
                # update all collapsed tiles
                grid.update_tiles(lookup)

                # while uncollapsed tiles still exist
                while len(unsure_tiles) > 0:
                    # get tile with lowest entropy
                    lowest_entropy_tile = grid.get_lowest_entropy(unsure_tiles)

                    # collapse and remove
                    lowest_entropy_tile.collapse()
                    unsure_tiles.remove(lowest_entropy_tile)

                    # update all tiles
                    grid.update_tiles(lookup)

                # if all tiles have same final state, take as error
                if all([tile.final_state == grid.flat_tiles[0].final_state for tile in grid.flat_tiles]):
                    continue

                print(f'Image successfully generated after {i + 1} attempts.')
                return grid.as_image(resize)
            
            except (ValueError, Exception):
                if verbose:
                    filled = ((grid.shape.w * grid.shape.h) - len(unsure_tiles)) / (grid.shape.w * grid.shape.h)
                    print(f'Attempt {i + 1: >{len(str(max_tries))}}: {filled * 100:.2g}% filled')
                continue
        
        # if past max tries and no image returned
        else:
            raise Exception(f'Generation terminated after {max_tries} attempts.')

    def get_lowest_entropy(self, tiles: list[Tile] = None) -> Tile:
        if tiles is None:
            tiles = deepcopy(self.flat_tiles)

        # flatten and sort tiles array based on entropy
        tiles = list(filter(lambda tile: not tile.is_collapsed, tiles))
        tiles.sort(key=lambda tile: tile.entropy)

        # if one left
        if len(tiles) == 1:
            return tiles[0]

        # get tiles with lowest entropy (first sublist of entropies)
        tiles = [tile for tile in tiles if tile.entropy == tiles[0].entropy]

        # pick and return random tile from sublist
        return random.choice(tiles)
                
    def as_image(self, resize: tuple[int, int] = None) -> Image:
        # build pixel array
        pixel_arr = np.ones((self._tile_shape[0] * self.shape.h, self._tile_shape[1] * self.shape.w, self._tile_shape[2]))

        # iterate over tiles
        for y in range(self.shape.h):
            for x in range(self.shape.w):
                tile = self.tile_at(x, y)

                # if tile has been collapsed
                if tile.is_collapsed:
                    # set pixels in pixel arr
                    pixel_arr[
                        y * self._tile_shape[0]:y * self._tile_shape[0] + self._tile_shape[0],
                        x * self._tile_shape[1]:x * self._tile_shape[1] + self._tile_shape[1]
                    ] = self._tile_imgs[tile.final_state]

                else:
                    pixel_arr[
                        y * self._tile_shape[0]:y * self._tile_shape[0] + self._tile_shape[0],
                        x * self._tile_shape[1]:x * self._tile_shape[1] + self._tile_shape[1]
                    ] = np.ones(self._tile_shape)

        img = Image.fromarray((pixel_arr * 255).astype(np.uint8))

        if resize is not None:
            return img.resize(resize)
        return img
    
    def copy(self) -> Grid:
        grid = Grid(self.shape.w, self.shape.h, self._data_folder, self._verbose)

        grid._tile_shape = self._tile_shape
        grid._tile_imgs = self._tile_imgs

        grid._tiles = deepcopy(self._tiles)

        return grid
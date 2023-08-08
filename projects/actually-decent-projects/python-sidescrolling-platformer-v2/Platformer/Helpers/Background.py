from __future__ import annotations

import os

import pygame as pg


class Background:
    def __init__(self, base: pg.Surface, path: os.PathLike) -> None:
        self.base = base
        self.tile_image = pg.image.load(path)

        self.tile_pos = []

    def tile(self) -> None:
        width, height = self.base.get_width(), self.base.get_height()
        img_width, img_height = self.tile_image.get_width(), self.tile_image.get_height()

        # iterate over and fill the window area starting from top left
        for y in range(height // img_height + 1):
            for x in range(width // img_width + 1):
                self.tile_pos.append((x * img_height, y * img_height))

    def show(self) -> None:
        for position in self.tile_pos:
            self.base.blit(self.tile_image, position)
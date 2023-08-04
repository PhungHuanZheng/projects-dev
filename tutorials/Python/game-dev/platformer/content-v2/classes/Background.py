from __future__ import annotations

import os
import pygame


class Background:
    def __init__(self, base: pygame.Surface, asset_path: os.PathLike) -> None:
        self._base = base
        self._tile_image = pygame.image.load(asset_path)

        self._tile_pos = []

    def tile(self) -> None:
        width, height = self._base.get_width(), self._base.get_height()
        img_width, img_height = self._tile_image.get_width(), self._tile_image.get_height()

        # iterate over and fill the window area starting from top left
        for y in range(height // img_height + 1):
            for x in range(width // img_width + 1):
                self._tile_pos.append((x * img_height, y * img_height))

    def show(self) -> None:
        for position in self._tile_pos:
            self._base.blit(self._tile_image, position)
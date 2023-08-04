from __future__ import annotations

import os
import pygame


class Background:
    def __init__(self, asset_path: os.PathLike) -> None:
        # get image
        self._bg_image = pygame.image.load(asset_path)

    def tile(self, window: pygame.Surface) -> tuple[pygame.Surface, list[tuple[int, int]]]:
        width, height = window.get_width(), window.get_height()
        img_width, img_height = self._bg_image.get_width(), self._bg_image.get_height()
        return_val: tuple[pygame.Surface, list[tuple[int, int]]] = (self._bg_image, [])

        # iterate over and fill the window area starting from top left
        for y in range(height // img_height + 1):
            for x in range(width // img_width + 1):
                return_val[1].append((x * img_height, y * img_height))

        # return data structure
        return return_val
    
    def show(self, window: pygame.Surface, image: pygame.Surface, positions: list[tuple[int, int]]) -> None:
        # draw and update window
        for pos in positions:
            window.blit(image, pos)
        pygame.display.update()

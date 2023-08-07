from __future__ import annotations

import os
from copy import deepcopy
from typing import Literal
from pathlib import Path
import pygame


class SpriteSheet:
    def __init__(self, path: os.PathLike) -> None:
        """
        Instantiates a `SpriteSheet` object. 

        Parameters
        ----------
        `path` : `PathLike`
            File path to a single sprite sheet
        """

        # check that path leads to a loadable image
        if not os.path.isfile(path):
            raise ValueError(f'"{path}" is not a filepath to an image.')

        # basic init
        self._path = path
        self._raw_sprite_sheet: pygame.Surface = pygame.image.load(path)
        self._sprites: list[pygame.Surface] = [self._raw_sprite_sheet.convert_alpha()]
        self._n_frames = 1

    @property
    def sprites(self) -> list[pygame.Surface]:
        return self._sprites
    
    @property
    def n_frames(self) -> int:
        return self._n_frames
    
    def animate(self, frame_width: int, frame_height: int) -> SpriteSheet:
        # get longer side and assume thats the animation axis
        img_width, img_height = self._raw_sprite_sheet.get_width(), self._raw_sprite_sheet.get_height()
        long_side = img_width if img_width > img_height else img_height
        short_side = img_width if img_width < img_height else img_height

        # check that sides are perfectly divisible by the frame width and height
        if img_width % frame_width != 0:
            raise ValueError(f'Sprite sheet width ({img_width}) and the frame width passed ({frame_width}) are not perfectly divisible.')
        if img_height % frame_height != 0:
            raise ValueError(f'Sprite sheet width ({img_height}) and the frame width passed ({frame_height}) are not perfectly divisible.')

        # check that short side length matches at least one frame side length
        if short_side != frame_width and short_side != frame_height:
            raise ValueError(f'Expecting a single row or column of sprites for animation, got {img_height // frame_height} '+
                             f'rows and {img_width // frame_width} colums instead.')

        # get sprite animation data, clear current sprite list
        self._n_frames = long_side // (frame_width if img_width > img_height else frame_height)
        self._sprites.clear()

        # iterate over frames and extract 
        for i in range(self._n_frames):
            # create empty image to put frame on
            surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * frame_width if long_side == img_width else 0, 
                                i * frame_height if long_side == img_height else 0,
                                frame_width, frame_height)

            # draw from to surface and append
            surface.blit(self._raw_sprite_sheet, (0, 0), rect)
            self._sprites.append(surface)

        return self

    def isolate(self, x: int, y: int, width: int, height: int) -> SpriteSheet:
        surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        rect = pygame.Rect(x, y, width, height)
        surface.blit(self._raw_sprite_sheet, (0, 0), rect)
        self._raw_sprite_sheet = surface
        self._sprites = [self._raw_sprite_sheet]

        return self

    def scale(self, scale: float) -> SpriteSheet:
        for i, frame in enumerate(self._sprites):
            self._sprites[i] = pygame.transform.scale_by(frame, scale)

        return self

    def flip(self, flip_x: bool = False, flip_y: bool = False) -> SpriteSheet:
        for i, frame in enumerate(self._sprites):
            self._sprites[i] = pygame.transform.flip(frame, flip_x, flip_y)
        return self

    def copy(self) -> SpriteSheet:
        copy_sheet = SpriteSheet(self._path)
        copy_sheet._sprites = self._sprites[:]
        copy_sheet._n_frames = self._n_frames
        return copy_sheet
        

from __future__ import annotations

import os
from typing import Literal

import pygame as pg


class SpriteSheet:
    """
    Object representation of a spritesheet used in 2D games.

    Attributes
    ----------
    

    Methods
    -------
    
    """

    ANIMATION_FRAMECOUNTER = {}
    ORDERED_DIRECTIONS = ('UP', 'RIGHT', 'DOWN', 'LEFT')

    def __init__(self, path: os.PathLike) -> None:
        # load image
        self.__path = path
        self.__raw = pg.image.load(path).convert_alpha()
        self.name = os.path.splitext(os.path.basename(path))[0]

        # image attributes
        self.width = self.__raw.get_width()
        self.height = self.__raw.get_height()

        # animation attributes
        self._n_frames = 1
        self._frames = [self.__raw.copy()]

    def animate(self, frame_width: int, frame_height: int, axis: Literal['HORIZONTAL', 'VERTICAL']) -> SpriteSheet:
        """
        Animates the spritesheet, changing the `SpriteSheet._n_frames` and `SpriteSheet.
        _frames` attributes. Uses the "frame_width" and "frame_height" parameters
        passed to slice the raw spritesheet into frames.

        Parameters
        ----------
        `frame_width` : `int`
            The width of each animation frame in pixels.
        `frame_height` : `int`
            The height of each animation frame in pixels.
        `axis` : `Literal['HORIZONTAL', 'VERTICAL']`
            Specifies the animation axis to slice frames from.
        """

        # check animation axis and get axis lengths
        if axis == 'HORIZONTAL':
            if self.__raw.get_width() % frame_width != 0:
                raise ValueError(f'The spritesheet width and the frame_width passed must be perfectly divisible ' +
                                 f'for axis=HORIZONTAL, got a remainder of {self.__raw.get_width() % frame_width} ' +
                                 f'pixels.')
            self._n_frames = self.__raw.get_width() // frame_width
            self._frames.clear()

        elif axis == 'VERTICAL':
            if self.__raw.get_height() % frame_height != 0:
                raise ValueError(f'The spritesheet height and the frame_height passed must be perfectly divisible ' +
                                 f'for axis=VERTICAL, got a remainder of {self.__raw.get_height() % frame_height} ' +
                                 f'pixels.')
            self._n_frames = self.__raw.get_height() // frame_height
            self._frames.clear()

        else:
            raise ValueError(f'Expecting an "axis" parameter of either "HORIZONTAL" or "VERTICAL", got "{axis}" instead.')

        # isolate frames from raw spritesheet
        for i in range(self._n_frames):
            surface = pg.Surface((frame_width, frame_height), pg.SRCALPHA, 32)
            rect = pg.Rect(i * frame_width if axis == 'HORIZONTAL' else 0, 
                           i * frame_height if axis == 'VERTICAL' else 0,
                           frame_width, frame_height)

            # draw from to surface and append
            surface.blit(self.__raw, (0, 0), rect)
            self._frames.append(surface.convert_alpha())

        # method chaining
        return self

    def display_on(self, base: pg.Surface, pos: tuple[int, int], interval: int = 1) -> None:
        """
        SpriteSheet testing method, not to be used extensively. Use `pg.Surface.blit` 
        for displaying sprites on `Surface` instances.

        Parameters
        ----------
        `base` : `Surface`
            Pygame `Surface` instance to show this sprite/animation on.
        `pos` : `tuple[int, int]`
            Position to show this sprite/animation at.
        `interval` : `int`, `default = 1`
            Interval in ticks (FPS) between animation frames
        """
        
        # add to internal frame tracker
        if self.name not in SpriteSheet.ANIMATION_FRAMECOUNTER:
            SpriteSheet.ANIMATION_FRAMECOUNTER[self.name] = 0
        
        # adjust interval and put sprite on screen
        if interval > 1 and isinstance(interval, int):
            temp_frames = [frame for frame in self._frames for _ in range(interval)]
            base.blit(temp_frames[SpriteSheet.ANIMATION_FRAMECOUNTER[self.name]], pos)
        base.blit(self._frames[SpriteSheet.ANIMATION_FRAMECOUNTER[self.name]], pos)

        # update frame tracker
        SpriteSheet.ANIMATION_FRAMECOUNTER[self.name] = (SpriteSheet.ANIMATION_FRAMECOUNTER[self.name] + 1) % self._n_frames

    def copy(self) -> SpriteSheet:
        """
        Creates and returns a copy of this `SpriteSheet` instance.

        Returns
        -------
        `SpriteSheet`
            Copy of this `SpriteSheet` instance.
        """

        new_sheet = SpriteSheet(self.__path)
        new_sheet._n_frames = self._n_frames
        new_sheet._frames = [frame.copy() for frame in self._frames]

        return new_sheet
    
    def to_dict(self, directional: bool = False, facing: Literal['LEFT', 'RIGHT'] = 'RIGHT') -> dict[str, SpriteSheet]:
        """
        Converts this spritesheet to a dictionary and returns it. Optionally add directionality 
        to the sprites. If the "directions" parameter is passed, the "facing" parameter must be 
        passed as well or it will default to "RIGHT". If `directional`, the direction will be added
        to the spritesheet name in the dictionary passed as 'basename_{DIRECTION}'.

        Parameters
        ----------
        `directional` : `bool`, `default = False`
            Whether or not to add directionality.
        `facing` : `Literal['LEFT', 'RIGHT']`, `default = 'RIGHT'`
            Initial facing direction of the sprite

        Returns
        -------
        `dict[str, SpriteSheet]`
            Dictionary of spritesheet names and `SpriteSheet` instance key value pairs.
        """

        # if no directions, just return self with base name
        if not directional:
            return {self.name: self.copy()}
        
        directional_dict = {}
        for direction in ('LEFT', 'RIGHT'):
            if facing == direction:
                # facing same direction
                facing_sheet = self.copy()
                facing_sheet._frames = [frame.copy() for frame in self._frames]
                facing_sheet.name = f'{self.name}_{facing}'
                directional_dict[f'{facing_sheet.name}_{facing}'] = facing_sheet

            else:
                # facing other direction
                other_sheet = self.copy()
                other_sheet._frames = [pg.transform.flip(frame, True, False).convert_alpha() for frame in self._frames]
                other_sheet.name = f'{self.name}_{direction}'
                directional_dict[f'{other_sheet.name}_{direction}'] = other_sheet

        return directional_dict
from __future__ import annotations

import os
import uuid
from typing import Literal

import pygame as pg


class SpriteSheet:
    SUPPORTED_EXTENSIONS = ('png', 'jpg')

    def __init__(self, path: os.PathLike | str) -> None:
        # check that path leads to a loadable image
        SpriteSheet._check_path(path)
        self.__path = path

        # init basic attributes
        self.name = os.path.splitext(os.path.basename(path))[0]
        self.raw = pg.image.load(path).convert_alpha()
        self.sprites: list[pg.Surface] = [self.raw]
        self.n_frames = 1

        # mask initiated when related entity is registered
        self.masks: list[pg.Mask] = []
    
    @staticmethod
    def _check_path(path: os.PathLike | str) -> None:
        # check that path leads to a loadable image
        if not os.path.isfile(path):
            raise ValueError(f'"{path}" is not a filepath to an image.')
        if not any(path.endswith(ext) for ext in SpriteSheet.SUPPORTED_EXTENSIONS):
            raise ValueError(f'File extension "{os.path.splitext(path)[1]}" is not supported, ' + 
                             f'supported file extensions: {", ".join(SpriteSheet.SUPPORTED_EXTENSIONS)}.')

    @classmethod
    def isolate_from(cls, path: os.PathLike | str, x: int, y: int, width: int, height: int, *, name: str = None) -> SpriteSheet:
        """
        Isolates an area from a sprite sheet and extracts it as a single `SpriteSheet`
        instance. Useful for extracting a sprite or sprites from a spritesheet with 
        multiple different sprites.

        Parameters
        ----------
        `path` : `PathLike | str`
            Filepath to the spritesheet image file. Call `SpriteSheet.SUPPORTED_EXTENSIONS`
            for a list of supported image file extensions.
        `x` : `int`
            Starting x-position in pixels (left) of the sprite(s) to be extracted.
        `y` : `int`
            Starting y-position in pixels (top) of the sprite(s) to be extracted.
        `width` : int
            Width in pixels of the sprite(s) to be extracted.
        `height` : int
            Height in pixels of the sprite(s) to be extracted.
        `name` : `str`, `default = None`
            Name of the new `SpriteSheet` instance created. If left as `None`, a UUID will
            be generated as its name.

        Returns
        -------
        `SpriteSheet`
            `SpriteSheet` instance with the isolated sprite.
        """ 

        # check that path leads to a loadable image and load
        SpriteSheet._check_path(path)
        raw = pg.image.load(path).convert_alpha()
        
        # isolate sprite
        surface = pg.Surface((width, height), pg.SRCALPHA, 32)
        rect = pg.Rect(x, y, width, height)
        surface.blit(raw, (0, 0), rect)

        # create new SpriteSheet instance and assign attributes
        sheet = SpriteSheet(path)
        sheet.name = name if name is not None else str(uuid.uuid4())
        sheet.raw = surface
        sheet.sprites = [sheet.raw]
        sheet.n_frames = 1

        return sheet

    def animate(self, frame_width: int, frame_height, animation_axis: Literal[0, 1] = None) -> SpriteSheet:
        """
        Generates an animation from the current raw image at `SpriteSheet.raw`. Uses the 
        passed `frame_width` and `frame_height` to separate frames.

        Parameters
        ----------
        `frame_width` : `int`
            Width in pixels of each frame of the animation.
        `frame_height` : `int`
            Height in pixels of each frame of the animation.
        `animation_axis` : `int`, `default = None`
            Axis containing the animated frames. If `None`, assumes the longer
            side is the animation axis.

        Returns
        -------
        `SpriteSheet`
            This instance by reference for method chaining and variable assignment. 
            Updates this instances' `n_frames` and `sprites` with the frames as a 
            list of `pygame.Surface` instances.
        """

        # get animation axis
        if animation_axis is None:
            # get long side and assume thats the animation axis
            img_width, img_height = self.raw.get_width(), self.raw.get_height()
            animation_axis = img_width if img_width > img_height else img_height
            single_axis = img_width if img_width < img_height else img_height

        else:
            if animation_axis == 0:
                animation_axis = img_height
                single_axis = img_width

            elif animation_axis == 1:
                animation_axis = img_width
                single_axis = img_height

            else:
                raise ValueError(f'animation_axis parameter expects an integer of either 0 or 1, got "{animation_axis}" instead.')


            # check that sides are perfectly divisible by the frame width and height
        if img_width % frame_width != 0:
            raise ValueError(f'Sprite sheet width ({img_width}) and the frame width passed ({frame_width}) are not perfectly divisible.')
        if img_height % frame_height != 0:
            raise ValueError(f'Sprite sheet width ({img_height}) and the frame width passed ({frame_height}) are not perfectly divisible.')

        # check that short side length matches at least one frame side length
        if single_axis != frame_width and single_axis != frame_height:
            raise ValueError(f'Expecting a single row or column of sprites for animation, got {img_height // frame_height} ' +
                             f'rows and {img_width // frame_width} colums instead.')
        
        # get sprite animation data, clear current sprite list
        self.n_frames = animation_axis // (frame_width if img_width > img_height else frame_height)
        self.sprites.clear()

        # iterate over frames and extract 
        for i in range(self.n_frames):
            # create empty image to put frame on
            surface = pg.Surface((frame_width, frame_height), pg.SRCALPHA, 32)
            rect = pg.Rect(i * frame_width if animation_axis == img_width else 0, 
                                i * frame_height if animation_axis == img_height else 0,
                                frame_width, frame_height)

            # draw from to surface and append
            surface.blit(self.raw, (0, 0), rect)
            self.sprites.append(surface)

        return self

    def flip(self, flip_x: bool = False, flip_y: bool = False) -> SpriteSheet:
        """
        Flips sprites about the horizontal and/or vertical axis in-place.
        A wrapper for `pygame.transform.flip`.

        Parameters
        ----------
        `flip_x` : `bool`, `default = False`
            Whether or not to flip sprites about the vertical axis
        `flip_y` : `bool`, `default = False`
            Whether or not to flip sprites about the horizontal axis

        Returns
        -------
        `SpriteSheet` 
            The instance the method was called on for method chaining.
        """

        self.raw = pg.transform.flip(self.raw, flip_x, flip_y)
        self.sprites = [pg.transform.flip(sprite, flip_x, flip_y) for sprite in self.sprites]

        return self

    def scale(self, factor: float = 1) -> SpriteSheet:
        """
        Scales sprites by the `scale` passed. A wrapper for 
        `pygame.transform.scale_by`.

        Parameters
        ----------
        `factor` : `float`, `default = 1`
            Factor to scale sprites by.

        Returns
        -------
        `SpriteSheet` 
            The instance the method was called on for method chaining.
        """

        self.raw = pg.transform.scale_by(self.raw, factor)
        self.sprites = [pg.transform.scale_by(sprite, factor) for sprite in self.sprites]

        return self

    def copy(self, *, name: str = None) -> SpriteSheet:
        """
        Generates and returns a copy of this `SpriteSheet` instance. Passing the `name` 
        parameter changes the `name` attribute of the `SpriteSheet` instance returned.

        Parameters
        ----------
        `name` : `str`, `default = None`
            Name of the new `SpriteSheet` instance returned. Leave as `None` to not copy 
            the current `name`

        Returns
        -------
        `SpriteSheet` 
            Copied `SpriteSheet` instance.
        """

        sheet_copy = SpriteSheet(self.__path)
        sheet_copy.name = self.name if name is not None else name
        sheet_copy.raw = pg.Surface.copy(self.raw)
        sheet_copy.sprites = [pg.Surface.copy(sprite) for sprite in self.sprites]
        sheet_copy.n_frames = self.n_frames

        return sheet_copy

    def to_dict(self, facing: Literal['UP', 'RIGHT', 'DOWN', 'LEFT'] = None, directions: list[Literal['UP', 'RIGHT', 'DOWN', 'LEFT']] = None) -> dict[str, SpriteSheet]:
        """
        Returns this `SpriteSheet` instance as a Python dictionary of name and 
        `SpriteSheet`(s). If `directions` is passed with the appropriate 
        parameters, flips the sprite(s) in those directions and generates another
        `SpriteSheet` instance. 

        Parameters
        ----------
        `facing` : `Literal['UP', 'RIGHT', 'DOWN', 'LEFT']`
            Direction the sprite(s) is/are facing before flipping directionally.
        `directions` : `list[Literal['UP', 'RIGHT', 'DOWN', 'LEFT']]`, `default = None`
            Direction(s) to flip the sprite in. Leave as `None` to not flip the sprite.

        Returns
        -------
        `dict[str, SpriteSheet]`
            Dictionary of `SpriteSheet` instance names and instances.

        Examples
        --------
        Conversion to dictionary with directions
        >>> sheet = SpriteSheet('path/to/asset/asset.png')
        >>> sprites = sheet.to_dict('LEFT', directions=['LEFT', 'RIGHT'])
        >>> print(sprites)
        {'asset_LEFT': <__main__.SpriteSheet object at 0x2aba1c0cf691> 
         'asset_RIGHT': <__main__.SpriteSheet object at 0x2aba1c0cf890>}

        Conversion to dictionary without directions
        >>> sheet = SpriteSheet('path/to/asset/asset.png')
        >>> sprites = sheet.to_dict(directions=None)
        >>> print(sprites)
        {'asset': <__main__.SpriteSheet object at 0x2aba1c0cf691>}
        """

        # check that if directions are passed, facing is also passed
        if directions is not None and facing is None:
            raise ValueError(f'Directions "{directions}" were passed but no initial facing diretion was passed.')

        # no directions, return dict of 1 key/value pair
        if directions is None:
            return {self.name: self.copy()}
        
        # directions, return directional pairs
        dir_dict: dict[str, SpriteSheet] = {}
        
        # dont flip for current facing direction
        dir_dict[f'{self.name}_{facing}'] = self.copy(name=f'{self.name}_{facing}')

        if 'UP' in directions and facing != 'UP':
            dir_dict[f'{self.name}_UP'] = self.copy(name=f'{self.name}_UP').flip(flip_y=True)
        if 'RIGHT' in directions and facing != 'RIGHT':
            dir_dict[f'{self.name}_RIGHT'] = self.copy(name=f'{self.name}_RIGHT').flip(flip_x=True)
        if 'DOWN' in directions and facing != 'DOWN':
            dir_dict[f'{self.name}_DOWN'] = self.copy(name=f'{self.name}_DOWN').flip(flip_y=True)
        if 'LEFT' in directions and facing != 'LEFT':
            dir_dict[f'{self.name}_LEFT'] = self.copy(name=f'{self.name}_LEFT').flip(flip_x=True)


        return dir_dict





